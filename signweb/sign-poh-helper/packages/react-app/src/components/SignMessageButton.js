import { Button } from "./index";
import {ethers} from "ethers"

export default function SignMessageButton({ provider, message, onMessageSigned }) {

    async function signMessage() {
        const signer = provider.getSigner();
        if (signer && message) {
            console.log("SIGNER", signer)
            const signedMessage = await signer.signMessage(message);
            onMessageSigned(signedMessage)

            const address = ethers.utils.verifyMessage(message, signedMessage);
            console.log("VERIFIED MESSSAGE", address)
        }
        else {
            console.warn("No signer")
        }
    }

    return (
        <Button
            onClick={() => {
                if (provider) {
                    signMessage();
                }
            }}
        >
            Sign Message
        </Button>
    );
}