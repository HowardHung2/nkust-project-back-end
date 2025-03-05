require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");


module.exports = {
  solidity: "0.8.24",
  networks: {
    xrplEVM: {
      url: process.env.XRPL_EVM_URL,
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};