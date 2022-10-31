import {
  Keypair,
  Connection,
  PublicKey,
  LAMPORTS_PER_SOL,
  SystemProgram,
  TransactionInstruction,
  Transaction,
  sendAndConfirmTransaction,
} from "@solana/web3.js";
import fs from "mz/fs";
import path from "path";

const PROGRAM_KEYPAIR_PATH = path.join(
  path.resolve(__dirname, "../../dist/program"),
  "hello_solana-keypair.json"
);

async function main() {
  console.log("Launching client...");
  let connection = new Connection("https://api.devnet.solana.com", "confirmed");
  const secretKeyString = await fs.readFile(PROGRAM_KEYPAIR_PATH, {
    encoding: "utf8",
  });
  const secretKey = Uint8Array.from(JSON.parse(secretKeyString));
  const programKeypair: Keypair = Keypair.fromSecretKey(secretKey);
  let programId: PublicKey = programKeypair.publicKey;
  console.log(`programId is ${programId.toString()}`);

  const triggerKeypair = Keypair.generate();
  const airdropRequest = await connection.requestAirdrop(
    triggerKeypair.publicKey,
    LAMPORTS_PER_SOL
  );
  await connection.confirmTransaction(airdropRequest);

  console.log("--Printing Program ", programId.toBase58());
  const instruction = new TransactionInstruction({
    keys: [
      { pubkey: triggerKeypair.publicKey, isSigner: false, isWritable: true },
    ],
    programId,
    data: Buffer.alloc(0),
  });

  await sendAndConfirmTransaction(
    connection,
    new Transaction().add(instruction),
    [triggerKeypair]
  );
}

main();
