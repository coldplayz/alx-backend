import { createClient } from 'redis';

const subscriber = createClient();

subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

const channel = 'holberton school channel';

subscriber.subscribe(channel, (error) => {
  if (error) {
    throw new Error(error);
  }
});

subscriber.on('message', (channel, message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe(channel);
    subscriber.quit();
  }
});
