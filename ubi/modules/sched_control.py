from datetime import datetime, timedelta
from telethon import events
import asyncio
from ubi import u, s, admin_cmd , log

del_timeout = 1


def start_aps():
    s.start()
    log.info('Started scheduler.')


def remove_all_jobs():
    log.info('Removing all jobs...')
    s.remove_all_jobs()


def stop_aps():
    # s.remove_all_jobs()
    s.shutdown()
    print('Stopped scheduler.')


def list_jobs():
    print('Listing jobs...')
    for job in s.get_jobs():
    # :var str id: the unique identifier of this job
    # :var str name: the description of this job
    # :var func: the callable to execute
    # :var tuple|list args: positional arguments to the callable
    # :var dict kwargs: keyword arguments to the callable
    # :var bool coalesce: whether to only run the job once when several run times are due
    # :var trigger: the trigger object that controls the schedule of this job
    # :var str executor: the name of the executor that will run this job
    # :var int misfire_grace_time: the time (in seconds) how much this job's execution is allowed to
    #     be late (``None`` means "allow the job to run no matter how late it is")
    # :var int max_instances:
    # :var datetime.datetime next_run_time: the next scheduled run time of this job
        yield job


def sample_callback():
    print('Sample job callback called.')


def add_sample():
    s.add_job(sample_callback, 'interval', seconds=30)


@u.on(admin_cmd(pattern=".s start"))
async def scheduler_start(event):
    await event.edit('Starting aps...')
    start_aps()
    await event.edit('Aps operational.')
    await asyncio.sleep(del_timeout)
    await event.delete()


@u.on(admin_cmd(pattern=".s add sample"))
async def scheduler_start(event):
    await event.edit('Adding sample job ...')
    add_sample()
    await event.edit('Sample job scheduled every 10 seconds ...')
    await asyncio.sleep(del_timeout)
    await event.delete()


@u.on(admin_cmd(pattern=".s jobs"))
async def scheduler_start(event):
    try : 
        jobs = list(list_jobs())
        jobarr = []
        # print(jobs)
        for job in jobs:
            job_string = ""
            job_string += "JobID : " + job.id + "\n"
            job_string += "JobName : " + job.name + "\n"
            # job_string += str(job.func) + " "
            job_string += "Trigger : " + str(job.trigger) + "\n"
            # job_string += "Next run : " + timedelta(job.next_run_time , datetime.now())  + " seconds \n"
            # job_string += str(job.trigger) + " "
            # job_string += job.executor + " "
            # job_string += str(job.next_run_time) + " "
            # print(job_string)
            jobarr.append(job_string)
            print("Jobarr : ",jobarr)
        if jobs == [] : 
            await event.edit("No jobs active.")
        else :
            await event.edit("\n".join(jobarr))
    except Exception as e  : 
        await event.edit(e)
    # await asyncio.sleep(del_timeout)
    # await event.delete()


@u.on(admin_cmd(pattern=".s stop"))
async def scheduler_stop(event):
    await event.edit('Stopping aps...')
    stop_aps()
    await event.edit('Aps down.')
    await asyncio.sleep(del_timeout)
    await event.delete()
    
@u.on(admin_cmd(pattern=".s remjobs"))
async def scheduler_stop(event):
    await event.edit('Removing Jobs...')
    remove_all_jobs()
    await event.edit('Jobs removed.')
    await asyncio.sleep(del_timeout)
    await event.delete()
