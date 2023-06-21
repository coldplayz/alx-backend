import kue from 'kue';

import createPushNotificationsJobs from './8-job';

const queue = kue.createQueue();

const list = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4321 to verify your account',
  },
];
createPushNotificationsJobs(list, queue);

