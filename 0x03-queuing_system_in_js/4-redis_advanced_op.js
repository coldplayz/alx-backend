import { createClient, print } from 'redis';

const client = createClient();

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const hash = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const k in hash) {
  if (k in hash) {
    client.hset('HolbertonSchools', k, hash[k], (err, reply) => {
      print(err, reply);
    });
  }
}

client.hgetall('HolbertonSchools', (err, reply) => {
  console.log(reply);
});
