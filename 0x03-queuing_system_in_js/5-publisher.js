import { createClient } from 'redis';

const publisher = createClient();

publisher.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

publisher.on('connect', () => {
  console.log('Redis client connected to the server');
});

const channel = 'holberton school channel';

function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    publisher.publish(channel, message);
  }, time);
}

publishMessage('Holberton Student #1 starts course', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400);
