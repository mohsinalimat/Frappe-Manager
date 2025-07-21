import os
import re
import json
from pathlib import Path

from frappe_manager.compose_manager import DockerVolumeMount, DockerVolumeType
from frappe_manager.compose_manager.ComposeFile import ComposeFile
from frappe_manager.compose_project.compose_project import ComposeProject
from frappe_manager.display_manager.DisplayManager import richprint
from frappe_manager.docker_wrapper.DockerClient import DockerClient
from frappe_manager.migration_manager.backup_manager import BackupManager
from frappe_manager.migration_manager.migration_base import MigrationBase
from frappe_manager.migration_manager.migration_exections import (
    MigrationExceptionInBench,
)
from frappe_manager.migration_manager.migration_helpers import (
    MigrationBench,
    MigrationBenches,
    MigrationServicesManager,
)
from frappe_manager.migration_manager.version import Version


def get_container_name_prefix(site_name):
    return 'fm' + "__" + site_name.replace(".", "_")


def get_new_envrionment_for_service(service_name: str):
    envs = {
        "USERID": os.getuid(),
        "USERGROUP": os.getgid(),
        "SUPERVISOR_SERVICE_CONFIG_FILE_NAME": f"{service_name}.fm.supervisor.conf",
    }
    return envs


class MigrationV0180(MigrationBase):
    version = Version("0.18.0")

    def init(self):
        self.cli_dir: Path = Path.home() / "frappe"
        self.benches_dir = self.cli_dir / "sites"
        self.backup_manager = BackupManager(name=str(self.version), benches_dir=self.benches_dir)
        self.benches_manager = MigrationBenches(self.benches_dir)
        self.services_manager: MigrationServicesManager = MigrationServicesManager(
            services_path=self.cli_dir / "services"
        )
        self.pulled_images_list = []

    def migrate_bench(self, bench: MigrationBench):
        bench.compose_project.down_service(volumes=True)
        richprint.change_head("Migrating bench compose")

        if not bench.compose_project.compose_file_manager.exists():
            richprint.error(f"Failed to migrate {bench.name} compose file.")
            raise MigrationExceptionInBench(f"{bench.compose_project.compose_file_manager.compose_path} not found.")

        images_info = bench.compose_project.compose_file_manager.get_all_images()

        # images
        frappe_image_info = images_info["frappe"]
        frappe_image_info["tag"] = self.version.version_string()

        nginx_image_info = images_info["nginx"]
        nginx_image_info["tag"] = self.version.version_string()

        # change image nginx
        images_info["nginx"] = nginx_image_info

        # change image frappe, socketio, schedule
        images_info["frappe"] = frappe_image_info
        images_info["socketio"] = frappe_image_info
        images_info["schedule"] = frappe_image_info

        for image in [
            frappe_image_info,
            nginx_image_info,
            {'name': f'ghcr.io/rtcamp/frappe-manager-prebake', 'tag': self.version.version_string()},
        ]:
            pull_image = f"{image['name']}:{image['tag']}"
            if pull_image not in self.pulled_images_list:
                richprint.change_head(f"Pulling Image {pull_image}")
                output = DockerClient().pull(container_name=pull_image, stream=True)
                richprint.live_lines(output, padding=(0, 0, 0, 2))
                richprint.print(f"Image pulled [blue]{pull_image}[/blue]")
                self.pulled_images_list.append(pull_image)

        bench.compose_project.compose_file_manager.set_all_images(images_info)
        bench.compose_project.compose_file_manager.set_version(str(self.version))
        bench.compose_project.compose_file_manager.write_to_file()
        self.migrate_workers_compose(bench)

    def migrate_workers_compose(self, bench: MigrationBench):
        if bench.workers_compose_project.compose_file_manager.compose_path.exists():
            richprint.change_head("Migrating workers compose")
            workers_image_info = bench.workers_compose_project.compose_file_manager.get_all_images()

            for worker in workers_image_info.keys():
                workers_image_info[worker]["tag"] = self.version.version_string()

            bench.workers_compose_project.compose_file_manager.set_all_images(workers_image_info)
            bench.workers_compose_project.compose_file_manager.set_version(str(self.version))
            bench.workers_compose_project.compose_file_manager.write_to_file()

            richprint.print(f"Migrated [blue]{bench.name}[/blue] workers compose file.")
