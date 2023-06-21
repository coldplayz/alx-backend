// import { createClient } from 'redis';
import kue from 'kue';

// create a queue through which this process can push jobs to workers (other processes)
const push_notification_code = kue.createQueue();

const jobData = {
  phoneNumber: '08103665556',
  message: 'my phone number',
};

// create a job of type `first_job`
const job = push_notification_code.create('first_job', jobData);

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
  console.log('Notification job completed');
});

job.on('failed', (/* errMessage */) => {
  console.log('Notification job failed');
});
