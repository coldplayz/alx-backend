import kue from 'kue';

function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// create queue for collecting jobs to process
const processorQueue = kue.createQueue();

// write a processor for jobs with type `first_job`
processorQueue.process('first_job', (job, done) => {
  try {
    sendNotification(job.data.phoneNumber, job.data.message);
    done();
  } catch (err) {
    done(err);
  }
});
