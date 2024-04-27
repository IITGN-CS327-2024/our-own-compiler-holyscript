// JS loader and tester for the sample.
//
// Eli Bendersky [https://eli.thegreenplace.net]
// This code is in the public domain.
const fs = require('fs');
const path = require('path');
const assert = require('node:assert');

(async () => {
    // Load the WASM file and instantiate it.
    const bytes = fs.readFileSync(path.join(__dirname, 'wasm', 'arthimetic.wasm'));
    let obj = await WebAssembly.instantiate(new Uint8Array(bytes));

    const a = 1;
    const b = 8;
    let result = obj.instance.exports.add(a, b);
    console.log(`${a} + ${b} = ${result}`);
    assert.equal(result, a + b);
    result = obj.instance.exports.sub(a, b);
    console.log(`${a} - ${b} = ${result}`);
    assert.equal(result, a - b);
    result = obj.instance.exports.mul(a, b);
    console.log(`${a} * ${b} = ${result}`);
    assert.equal(result, a * b);
    result = obj.instance.exports.div(a, b);
    console.log(`${a} / ${b} = ${result}`);
    assert.equal(result, Math.trunc(a/b));
    result = obj.instance.exports.mod(a, b);
    console.log(`${a} % ${b} = ${result}`);
    assert.equal(result, a % b);

})();


