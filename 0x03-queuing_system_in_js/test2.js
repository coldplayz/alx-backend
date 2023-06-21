import { createClient } from 'redis';

const client = createClient();

client.on('error', (err) => console.log('Redis Client Error', err));

// await client.connect();

// client.set('key', 'value');

client.get('Holberton', (err, res) => {
  if (err) {
    console.error(err);
  } else {
    console.log(res);
  }
});

// await client.disconnect();
