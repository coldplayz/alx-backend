import { createClient } from 'redis';
import kue from 'kue';

const express = require('express');
const util = require('util');

// Redis
const client = createClient();

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

function reserveSeat(number) {
  client.set('available_seats', number/* , Callback[err, reply] */);
}

const get = util.promisify(client.get);

// returns a Promise itself
async function getCurrentAvailableSeats() {
  // get() returns a Promise which is awaited for the result
  const availableSeats = await get.call(client, 'available_seats');
  return availableSeats;
}

// Kue
const queue = kue.createQueue();

// Express
const app = express();

let reservationEnabled = true; // when seats are available

app.get('/available_seats', (req, res/* , next */) => {
  getCurrentAvailableSeats().then((availableSeats) => {
    res.json({ numberOfAvailableSeats: availableSeats });
  }).catch((err) => {
    console.log('/available_seats error:', err);
  });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
  } else {
    // create and queue a job
    const job = queue.create('reserve_seat', { number: 25 }/* data */); // TODO: dynamic data
    job.save((err) => {
      if (err) {
        // error during saving
        res.json({ status: 'Reservation failed' });
      } else {
        // successfully saved and added job to Redis
        res.json({ status: 'Reservation in process' });
      }
    });

    job.on('complete', (/* result */) => {
      console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (errMessage) => {
      console.log(`Seat reservation job ${job.id} failed: ${errMessage}`);
    });
  }
});

app.get('/process', (req, res) => {
  // const processorQueue = kue.createQueue();

  // return a response and continue processing
  res.json({ status: 'Queue processing' });

  // process the queue of `reserve_seat` jobs

  // processor logic that uses sendNotification to handle notification jobs; 2 jobs in parallel
  queue.process('reserve_seat', 2/* concurrency */, (job, done) => {
    // for each job...
    getCurrentAvailableSeats().then((availableSeats) => {
      const newAvailable = availableSeats - 1;
      reserveSeat(newAvailable);

      if (newAvailable === 0) {
        reservationEnabled = false;
      }

      if (newAvailable >= 0) {
        done();
      } else {
        // available seats is sub-zero; should get to this point because of reservationEnabled flag
        done(new Error('Not enough seats available'));
      }
    }).catch((err) => {
      console.log('/process error:', err);
    });
  });
});

// initialize available seats to 50
reserveSeat(50);

const port = 1245;
app.listen(port, () => {
  console.log(`app listening on port ${port}`);
});

module.exports = app;
