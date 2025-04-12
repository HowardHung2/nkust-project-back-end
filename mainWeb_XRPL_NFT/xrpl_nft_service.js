// 引入 xrpl 函式庫
const xrpl = require("xrpl")

// 建立連線 Client
const client = new xrpl.Client("wss://s.devnet.rippletest.net:51233")

async function connectAndGetAccount() {
  await client.connect()
  const wallet = xrpl.Wallet.generate()

  const response = await client.fundWallet(wallet)
  console.log("Funded wallet address:", response.wallet.address)

  await client.disconnect()
}

// 匯出功能供其他 JS 使用
module.exports = {
  connectAndGetAccount
}
