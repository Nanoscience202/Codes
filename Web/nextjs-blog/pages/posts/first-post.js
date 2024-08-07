import Link from "next/link";

import Head from "next/head";
import Script from "next/script";

import Layout from "../../components/layout";

function FirstPost() {
  return (
    <Layout>
      <Head>
        <title>First Post</title>
        <Script
          src="https://connect.facebook.net/en_US/sdk.js"
          strategy="lazyOnload"
          onLoad={() =>
            console.log("Script loaded crrectly, window.FB has been populated.")
          }
        />
      </Head>
      <h1>First Post</h1>
      <Link href="/">Home</Link>
    </Layout>
  );
}

export default FirstPost;
