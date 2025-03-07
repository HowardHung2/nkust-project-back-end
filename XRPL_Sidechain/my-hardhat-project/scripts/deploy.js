const HelloWorldModule = require("../ignition/modules/HelloWorld"); 

async function getInitialMessage() {
  // Mock function to simulate an asynchronous operation
  return "Hello, XRPL EVM!";
}

async function main() {
  const initialMessage = await getInitialMessage();

  if (initialMessage) {
    const { helloWorld } = await hre.ignition.deploy(HelloWorldModule, {
      parameters: { HelloWorldModule: { initialMessage } },
    });

    console.log(`HelloWorld deployed to: ${await helloWorld.getAddress()}`);

    // Fetch the initial message from the contract
    const message = await helloWorld.message();
    console.log("Initial message in contract:", message);
  } else {
    console.log("Initial message is undefined, skipping deployment.");
  }
}

main().catch(console.error);