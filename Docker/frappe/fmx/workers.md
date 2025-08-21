# Restarting Frappe Services Without Breaking Things

You need to restart your Frappe services. Sounds simple, right? Just run `fmx restart` and you're done!

<MarginNote>Restarting isn’t always straightforward—production systems require extra care to avoid data loss or user disruption.</MarginNote>

Not quite. If you're running a production system, there’s more to consider. Background workers may be processing important tasks, and if you stop them mid-job, you risk data corruption or unhappy users.

This guide will help you understand your options so you can restart services safely.

## What Actually Happens During a Restart?

When Frappe restarts, several components are recycled:
- **Web server** (Gunicorn/Nginx): Stops serving requests, then restarts
- **Background workers**: Are terminated and replaced with new ones
- **Scheduler**: The cron job trigger also restarts

During this process, your site is temporarily unavailable. The key question: how do you manage background jobs that might be running?

## Background Workers: The Hidden Heroes

Background workers handle behind-the-scenes tasks such as:
- Sending emails
- Generating reports
- Processing bulk operations
- Running scheduled tasks

If you terminate a worker halfway through updating 10,000 records, you can imagine the consequences.

## Check What's Running First

Before restarting, check the current activity:

**Quick check with bench:**
```bash
# default site
bench doctor 

# Or for a specific site:
bench --site your.site.name doctor
```

**Check the web interface:**
Go to `/app/rq-jobs` in your Frappe site to view active jobs and queues.

## Your Restart Options

### 1. `fmx restart` (The Default)

**What it does:** Sends a "please stop" signal to all processes. Workers get a grace period to finish, then are forcibly killed if they don’t.

**When to use:**
- Development environments
- Emergencies when you need services back ASAP
- When no critical jobs are running

**Pros:** Fast
**Cons:** Jobs may be interrupted

### 2. `fmx restart --wait-workers` (The Safe Option)

**What it does:**
- Tells Redis to stop accepting new jobs
- Waits for all current jobs to finish
- Restarts services only after jobs are done
- Resumes normal operation afterward

**When to use:**
- Production environments
- When critical jobs are running
- Before database migrations
- Anytime data integrity matters

**Pros:** Maximum safety, no job interruption
**Cons:** Can take longer if jobs are lengthy

### 3. `fmx restart --no-wait-workers` (The Middle Ground)

**What it does:**
- Tells Redis to stop accepting new jobs
- Signals workers to finish current jobs gracefully
- Restarts services immediately
- Old workers may still finish in the background

**When to use:**
- You want RQ coordination but can’t wait
- Routine updates where service availability is a priority
- Jobs are typically short-running

**Pros:** Faster, provides some coordination
**Cons:** No guarantee jobs finish before workers are replaced

### 4. `fmx restart --suspend-rq` (The Coordinator)

**What it does:**
- Suspends job processing via a Redis flag
- Performs a normal restart without waiting
- Resumes job processing afterward

**When to use:**
- You want RQ coordination without waiting
- Testing restart procedures

## Database Migrations

If you’re running `fmx restart --migrate`, you’re changing the database structure. This is critical:

<MarginNote>Always use `--wait-workers` with migrations to ensure jobs finish before the database changes.</MarginNote>

- **Good:** `fmx restart --migrate --wait-workers`
  - Jobs finish with the old database structure
  - Database is updated
  - New workers start with the new structure
  - Consistency is maintained

- **Bad:** `fmx restart --migrate --no-wait-workers`
  - Database changes while old workers are still running
  - Old workers access data that no longer matches expectations
  - Leads to errors and corruption

## How to Choose

Here’s a simplified decision process:

**Is your system completely broken?**
→ Use `fmx restart` for quick recovery

**Are critical jobs running that must finish?**
→ Use `fmx restart --wait-workers`

**Is this a database migration?**
→ Use `fmx restart --migrate --wait-workers` (do not skip this)

**Is this production and you want safety?**
→ Use `fmx restart --wait-workers`

**Is this development and you want speed?**
→ Use `fmx restart`

**Need a balance between speed and safety?**
→ Use `fmx restart --no-wait-workers`

## Common Scenarios

**Deploying new code to production:**
- No database changes: `fmx restart --no-wait-workers`
- With database changes: `fmx restart --migrate --wait-workers`

**Developing and restarting frequently:**
- Use `fmx restart` for speed

**Something’s broken and users are complaining:**
- If system is down: `fmx restart` (quick fix)
- If system is unstable: `fmx restart --wait-workers` (protect running jobs)

**Need to restart but a big report is running:**
- Use `fmx restart --wait-workers` and take a break

## Useful Options

- `--wait-workers-timeout 300`: Set a maximum wait time (default: 5 minutes)
- `--migrate-timeout 600`: Extend time for migrations if needed
- `--wait-workers-verbose`: See worker activity while waiting
- `--force-kill-timeout 30`: Force kill processes after 30 seconds

## When Things Go Wrong

**Workers won’t stop:**
- Check `fmx status -v` for stuck processes
- Review Background Jobs in the web interface
- Increase the timeout or use `--force-kill-timeout`

**RQ suspension fails:**
- Check your Redis connection in `common_site_config.json`
- Ensure Redis is running

**Services won’t start after restart:**
- View logs with `fmx logs [service_name] --tail 100`

<MarginNote>The `fmx restart` command is powerful—choose wisely to keep users happy and data safe.</MarginNote>
