// 部署智能合約(點火模組)，指定要部署哪個合約、需要哪些參數，以及如何管理部署流程

const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules"); //這個函式用於定義 Ignition 部署模組

module.exports = buildModule("HelloWorldModule", (m) => { //"HelloWorldModule"是該模組的名稱 (m) => { ... }是一個包含部署邏輯的回呼函數。
  const initialMessage = m.getParameter("initialMessage"); //這裡我們使用 m.getParameter("initialMessage") 來獲取部署參數
  const helloWorld = m.contract("HelloWorld", [initialMessage]); //這行程式碼部署 HelloWorld 合約，並將 initialMessage 作為建構函式的引數。

  return { helloWorld }; // 回傳 helloWorld 物件，讓其他程式可以使用這個合約實例。
});