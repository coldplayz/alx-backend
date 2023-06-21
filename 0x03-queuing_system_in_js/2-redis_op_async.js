import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, reply) => {
    print(err, reply);
  });
}

// turns a function, whose last arg is an error-first callback, into one returning a promise
const get = promisify(client.get);

async function displaySchoolValue(schoolName) {
  // use call() method and pass the object (client) whose
  // method we are promisifying, because get() accesses `this`
  const reply = await get.call(client, schoolName);
  console.log(reply);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
