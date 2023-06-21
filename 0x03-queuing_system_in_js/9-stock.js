import { createClient, print } from 'redis';

const express = require('express');
const util = require('util');

const client = createClient();

client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const app = express();

const listProducts = [
  {
    id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

function getItemById(id) {
  for (const obj of listProducts) {
    if (obj.id === id) {
      return obj;
    }
  }
  return {};
}

function reserveStockById(itemId, stock) {
  const key = `item.${itemId}`;
  // increase the number of stock reserved
  client.incrby(key, stock, (err, reply) => {
    print(err, reply);
  });
}

const get = util.promisify(client.get);

// returns a Promise
async function getCurrentReservedStockById(itemId) {
  const key = `item.${itemId}`;
  // console.log(key); // SCAFF
  const reservedStock = await get.call(client, key);

  return reservedStock; // null if key doesn't exist in redis
}

app.get('/list_products', (req, res/* , next */) => {
  const productList = [];
  const keys1 = ['id', 'name', 'price', 'stock'];
  const keys2 = ['itemId', 'itemName', 'price', 'initialAvailableQuantity'];
  const listSize = keys1.length;

  for (const obj of listProducts) {
    const obj2 = {};
    for (let i = 0; i < listSize; i += 1) {
      obj2[keys2[i]] = obj[keys1[i]];
    }
    productList.push(obj2);
  }

  res.json(productList);
});

app.get('/list_products/:itemId([0-9]+)', (req, res) => {
  const keys1 = ['id', 'name', 'price', 'stock'];
  const keys2 = ['itemId', 'itemName', 'price', 'initialAvailableQuantity'];
  const listSize = keys1.length;
  const obj0 = getItemById(Number(req.params.itemId)); // from listProducts

  if (Object.keys(obj0).length === 0) {
    // item with that itemId does not exist
    res.json({ status: 'Product not found' });
    return;
  }

  const obj2 = {};
  for (let i = 0; i < listSize; i += 1) {
    obj2[keys2[i]] = obj0[keys1[i]];
  }

  // determine current available stock and append that data
  getCurrentReservedStockById(obj2.itemId).then((reservedStock) => {
    let reserved = reservedStock;
    if (reservedStock === null) {
      reserved = 0;
    }
    // console.log(reserved); // SCAFF
    const currentQuantity = obj0.stock - reserved;
    obj2.currentQuantity = currentQuantity;
    res.json(obj2);
  }).catch((err) => {
    console.log('My route error:', err);
  });
});

app.get('/reserve_product/:itemId([0-9]+)', (req, res) => {
  const obj0 = getItemById(Number(req.params.itemId)); // from listProducts

  if (Object.keys(obj0).length === 0) {
    // item with that itemId does not exist
    res.json({ status: 'Product not found' });
    return;
  }

  // item exists; ensure there is, at least, one stock left
  getCurrentReservedStockById(obj0.id).then((reservedStock) => {
    let reserved = reservedStock;
    if (reservedStock === null) {
      reserved = 0;
    }

    // console.log(reserved); // SCAFF

    const currentQuantity = obj0.stock - reserved;
    if (currentQuantity > 0) {
      // enough stock left for one reservation
      reserveStockById(obj0.id, 1);
      res.json({ status: 'Reservation confirmed', itemId: obj0.id });
    } else {
      // not enough stock available for a reservation
      res.json({ status: 'Not enough stock available', itemId: obj0.id });
    }
  }).catch((err) => {
    console.log('/reserve_product error:', err);
  });
});

const port = 1245;
app.listen(port, () => {
  console.log(`app listening on port ${port}`);
});

module.exports = app;
