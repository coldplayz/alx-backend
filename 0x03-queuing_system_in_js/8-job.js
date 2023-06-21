// import kue from 'kue';

export default function createPushNotificationsJobs(jobs, queue) {
  if (!(jobs instanceof Array)) {
    // only arrays are allowed
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((jobData) => {
    // create a job of type `notification`
    const job = queue.create('notification', jobData);

    // add job to redis, which uses pub/sub system
    job.save((err) => {
      if (err) {
        console.log(err);
      } else {
        console.log(`Notification job created: ${job.id}`);
      }
    });

    // define event handlers (the callbacks)
    job.on('complete', (/* result */) => {
      console.log(`Notification job ${job.id} completed`);
    });

    job.on('failed', (errMessage) => {
      console.log(`Notification job ${job.id} failed: ${errMessage}`);
    });

    job.on('progress', (progress/* , data */) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  });
}
