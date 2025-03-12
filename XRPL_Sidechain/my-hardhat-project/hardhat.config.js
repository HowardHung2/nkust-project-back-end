require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();
require("@nomicfoundation/hardhat-verify");

module.exports = {
  solidity: "0.8.24",
  networks: {
    xrplEVM: {
      url: process.env.XRPL_EVM_URL,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
  networks: {
    'xrpl-evm': {
      url: 'https://rpc-evm-sidechain.xrpl.org'
    },
  },
  etherscan: {
    apiKey: {
      'xrpl-evm': 'empty'
    },
    customChains: [
      {
        network: "xrpl-evm",
        chainId: 1440002,
        urls: {
          apiURL: "https://explorer.xrplevm.org/api",
          browserURL: "https://explorer.xrplevm.org:3000"
        }
      }
    ]
  }

};



