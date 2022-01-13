import React, { useEffect, useState } from "react";

import { Body, Header } from "./components";
import WalletButton from "./components/WalletButton";
import SignMessageButton from "./components/SignMessageButton";
import useQueryString from "./hooks/useQueryString";
import useWeb3Modal from "./hooks/useWeb3Modal";


function App() {

  const [provider, loadWeb3Modal, logoutOfWeb3Modal] = useWeb3Modal();
  const queryString = useQueryString();
  const [hasSigner, setHasSigner] = useState(false)
  const [signedMessage, setSignedMessage] = useState("");

  function handleMessageSigned(signedMessage) {
    setSignedMessage(signedMessage);
  }

  useEffect(() => {
    if (provider && provider.getSigner()) {
      setHasSigner(true)
    }
  }, [provider])

  return (
    <div>
      <Header>

      </Header>
      <Body>
        Please, select the account registered on Proof of Humanity and then connect your wallet.
        <WalletButton provider={provider} loadWeb3Modal={loadWeb3Modal} logoutOfWeb3Modal={logoutOfWeb3Modal} />
        {hasSigner && queryString.get("tguid") ?
        <>Please, click on Sign message.
          <SignMessageButton provider={provider} message={queryString.get("tguid")} onMessageSigned={handleMessageSigned} />
          </> : <>Invalid user ID</>}
          {signedMessage && 
          <>Copy and paste this signed message on the bot <code><small>{signedMessage}</small></code></>}
      </Body>
    </div>
  );
}

export default App;
