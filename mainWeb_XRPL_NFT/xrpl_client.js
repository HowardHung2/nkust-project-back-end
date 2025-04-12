// In browsers, use a <script> tag. In Node.js, uncomment the following line:
const xrpl = require('xrpl')

// Wrap code in an async function so we can use await
async function connectClient() {

    // Define the network client
    const client = new xrpl.Client("wss://s.altnet.rippletest.net:51233")
    await client.connect()
    console.log("已連接 XRPL Devnet")

    // ... custom code goes here
    // 這裡可以做其他操作（例如：查詢帳戶、AMM、NFT 等）

    // Disconnect when done (If you omit this, Node.js won't end the process)
    await client.disconnect()
    console.log("已斷線 XRPL")
}

async function getAccount() {
    const client = new xrpl.Client("wss://s.devnet.rippletest.net:51233")
    await client.connect()

    // 建立並透過 Devnet 水龍頭領取 XRP 測試幣
    const fund_result = await client.fundWallet()
    const wallet = fund_result.wallet

    console.log("帳戶地址:", wallet.address)
    console.log("私密種子 (Seed):", wallet.seed)
    console.log("XRP 餘額:", await client.getXrpBalance(wallet.address))

    await client.disconnect()
}

async function queryAccountInfo() {
    const client = new xrpl.Client("wss://s.devnet.rippletest.net:51233")
    await client.connect()

    const address = "account_info"

    const response = await client.request({
        "command": "account_info",
        "account": address,
        "ledger_index": "validated"
    })

    const info = response.result.account_data
    console.log("XRP 餘額:", xrpl.dropsToXrp(info.Balance))
    console.log("交易序列號:", info.Sequence)

    await client.disconnect()
}


async function listenLedgerClose() {
    const client = new xrpl.Client("wss://s.devnet.rippletest.net:51233")
    await client.connect()
    console.log("連線成功，等待新 ledger...")

    // Listen to ledger close events
    client.request({
        "command": "subscribe",
        "streams": ["ledger"]
    })
    client.on("ledgerClosed", async (ledger) => {
        console.log(`Ledger #${ledger.ledger_index} validated with ${ledger.txn_count} transactions!`)
    })


}