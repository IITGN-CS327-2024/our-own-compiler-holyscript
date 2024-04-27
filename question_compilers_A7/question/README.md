# Contents

1. JavaScript Files- These call the files in the `wasm` folder and test each scenario.
2. WebAssembly Files- These are in the `wasm` folders.

# Description

There are 4 test cases:
1. Arithmetic- In this file the expected functions to be imported are `add`, `sub`, `mul`, `div` and `mod`. Each takes two integer inputs and returns an integer.

2. Caesar- In this file there two functions inputs, note that both functions return nothing:
	- `caesarEncrypt([int] plaintext, int plaintextLength, int key)`
	- `caesarDecrypt([int] plaintext, int plaintextLength, int key)`
Note that in the above the strings are converted to integer and then passed to the functions (a--> 0, b--> 1, etc.).

3. Sort array- In this file a single function is exported, note that the function return nothing:
	- `sort(int arr[], int length)`

# Submission

The submission will include the following:

1. The code for generating wat or wasm code. 

2. The code for the functions in your created language.

3. Command and requirements (dependencies like Python packages, etc.) we need to use to convert your code to `.wasm`.

4. The `.wat` or `.wasm` file created from the language.

Please note we will be running an automated test similar to the `test.sh` file. Hence, it is expected that the `.wasm` files name, etc. will match the files given in the `wasm` folder.