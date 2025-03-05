const HelloWorldModule = require("../ignition/modules/HelloWorld"); //引入 HelloWorld 模組

async function getInitialMessage() { //定義一個名為 getInitialMessage 的函數，是一個非同步函式，用來模擬取得初始訊息的操作（例如可能從 API 或資料庫取得資料）。
  // Mock function to simulate an asynchronous operation
  return "Hello, XRPL EVM!";
}

async function main() {  
  const initialMessage = await getInitialMessage(); //呼叫 getInitialMessage 函數，並將結果存入 initialMessage 變數。await 表示等待 getInitialMessage() 完成後，再將結果存入 initialMessage 變數。

  if (initialMessage) { //如果 initialMessage 不是 undefined，則執行部署合約的流程。
    const { helloWorld } = await hre.ignition.deploy(HelloWorldModule, { 
        // 使用 hre.ignition.deploy 函數部署 HelloWorld 模組，並將 initialMessage 作為參數傳入。
        // 第一個參數傳入 HelloWorldModule，這個模組定義了如何部署 HelloWorld 合約。
      parameters: { HelloWorldModule: { initialMessage } },
    } // 第二個參數是設定傳入部署模組的參數。這裡傳遞的參數物件中，針對 "HelloWorldModule" 模組，將 initialMessage 的值傳入合約建構函式中。
      // 部署成功後，回傳的物件中包含已部署的合約實例（命名為 helloWorld）。
    );

    console.log(`HelloWorld deployed to: ${await helloWorld.getAddress()}`);
    // 使用 helloWorld.getAddress() 取得合約地址，並將其輸出到終端機。

    // Fetch the initial message from the contract
    const message = await helloWorld.message(); // 使用 helloWorld.message() 取得合約中的訊息。
    console.log("Initial message in contract:", message);// 將合約中的訊息輸出到終端機。
  } else { 
    console.log("Initial message is undefined, skipping deployment."); //如果 initialMessage 是 undefined，則輸出訊息到終端機，並跳過部署流程。
  }
}

main().catch(console.error); //執行 main 函數，並在發生錯誤時輸出錯誤訊息到終端機。