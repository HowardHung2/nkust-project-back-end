// 導入 Web3 v4.x 正確寫法
const { Web3 } = require("web3");

// XRPL EVM Devnet RPC URL
const web3 = new Web3("https://rpc.xrplevm.org");

// 合約 ABI（只要一層 Array！）
const contractABI = [
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_message",
        "type": "string"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "message",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_message",
        "type": "string"
      }
    ],
    "name": "setMessage",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
];

// 合約地址
const contractAddress = "0x3796Ef7255AEd3c65f389F356066a30cc0feDa00";

// 合約實例
const contract = new web3.eth.Contract(contractABI, contractAddress);

// 包裝 async 函數
async function main() {
  try {
    // 讀取 message
    const result = await contract.methods.message().call();
    console.log("Current Message:", result);

    // // 發送交易
    // const senderAddress = "0xYourWalletAddress";
    // const privateKey = "0xYourPrivateKey";

    // const tx = {
    //   from: senderAddress,
    //   to: contractAddress,
    //   gas: 200000,
    //   data: contract.methods.setMessage("New Value").encodeABI()
    // };

    // const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);
    // const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);

    // console.log("Transaction Receipt:", receipt);

    // // 再次查詢 message
    // const updated = await contract.methods.message().call();
    // console.log("Updated Message:", updated);

  } catch (error) {
    console.error("Error:", error);
  }
}

main();
