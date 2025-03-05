const xrpl = require("xrpl");

async function getEthereumPrivateKey(secret) {
    // Generate wallet from XRPL secret
    const wallet = xrpl.Wallet.fromSeed(secret);
    console.log("XRPL Address:", wallet.classicAddress);
    console.log("Ethereum-Compatible Private Key:", wallet.privateKey);
}

const secretKey = "sEd7hDX5yKYU7aZxWjWsyasQMWMb49F"; // Replace with your actual secret
getEthereumPrivateKey(secretKey);
