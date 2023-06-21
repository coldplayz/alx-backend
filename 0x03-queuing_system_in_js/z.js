const { createClient } = require('redis');

async function getAwaited(callback, args) {
  // console.log(callback.name);
  try {
    const res = await callback(...args);
    return res;
  } catch (err) {
    console.log('Error in async func', err);
  }
  return 'Error';
}

const client = getAwaited(createClient, []);

(async function f1() {
  await client.on('error', (err) => console.log('Redis Client Error', err));
}());

getAwaited(client.connect, []);

// await client.set('key', 'value');
const value = getAwaited(client.get, ['key1']);
console.log(value);

getAwaited(client.disconnect, []);
