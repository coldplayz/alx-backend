const { createClient } = require('redis');

async function getAwaited() {
  // console.log(callback.name);
  try {
    const client = createClient();
    client.on('error', (err) => console.log('Redis Client Error', err));
    // await client.connect();

    const val = client.get('Holberton');
    console.log(val);
  } catch (err) {
    console.log('Error in async func', err);
  }
  return 'Error';
}

getAwaited();
