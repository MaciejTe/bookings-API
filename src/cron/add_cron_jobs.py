from crontab import CronTab


def add_cron_job_for_every_day_slots(cron_obj):
    """ Add cron job which adds daily slots generation.

    Args:
        cron_obj (CronTab): CronTab class object
    """
    activate_venv_cmd = 'source /booking_api/bin/activate'
    setup_cmd = 'cd /booking_api; python /booking_api/setup.py install'
    add_slots_cmd = 'python /booking_api/src/cron/add_slots_every_day.py'
    deactivate_venv_cmd = 'deactivate'
    cron_job_commands = [activate_venv_cmd, setup_cmd, add_slots_cmd,
                         deactivate_venv_cmd]

    with open("cron_job.sh", "w+") as cron_job_script:
        [cron_job_script.write(cmd + ' >> /var/log/cron.log 2>&1' + '\n')
         for cmd in cron_job_commands]

    job = cron_obj.new(command='bash /booking_api/cron_job.sh')
    job.hour.every(24)
    cron_obj.write()


if __name__ == "__main__":
    cron = CronTab(user='root')
    add_cron_job_for_every_day_slots(cron)
