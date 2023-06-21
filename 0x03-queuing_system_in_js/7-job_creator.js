import kue from 'kue';

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4153538781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4153718781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4159518782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account',
  },
];

// create a queue through which this process can push jobs to workers (other processes)
const push_notification_code_2 = kue.createQueue();

jobs.forEach((jobData) => {
  // create a job of type `notification`
  const job = push_notification_code_2.create('notification', jobData);

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
