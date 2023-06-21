import kue from 'kue';

const blacklist = ['4153518780', '4153518781'];

// logic to handle each notification job
function sendNotification(phoneNumber, message, job, done) {
  job.progress(0, 100/* , data */);

  if (blacklist.includes(job.data.phoneNumber)) {
    done(new Error(`Phone number ${job.data.phoneNumber} is blacklisted`));
  } else {
    job.progress(50, 100);
    console.log(`Sending notification to ${job.data.phoneNumber}, with message: ${job.data.message}`);
  }
}

const processorQueue = kue.createQueue();

// processor logic that uses sendNotification to handle notification jobs; 2 jobs in parallel
processorQueue.process('notification', 2/* concurrency */, (job, done) => {
  const { phoneNumber, message } = job.data;

  // error is handled in the function's logic
  sendNotification(phoneNumber, message, job, done);

  // everything worked OK
  done();
});
