const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules"); // 導入 buildModule 函式

module.exports = buildModule("HelloWorldModule", (m) => { // 這個函式呼叫建立了一個名為 "HelloWorldModule" 的部署模組。 第二個參數是一個回呼函式，函式中的 m 提供了用來取得部署參數和部署合約的工具。
  const initialMessage = m.getParameter("initialMessage"); // 透過 m.getParameter 取得一個名為 "initialMessage" 的參數，這個參數會傳遞給合約的建構子。
  const helloWorld = m.contract("HelloWorld", [initialMessage]); // 使用 m.contract 函式來部署名為 "HelloWorld" 的合約。第二個引數是一個陣列，裡面包含建構子所需的參數（在此例中，只有 initialMessage）。

  return { helloWorld }; // 回傳一個物件，其中包含剛剛部署好的 helloWorld 合約實例
});