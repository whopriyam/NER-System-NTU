import React, { Fragment } from "react";
import PropTypes from "prop-types";
import Document, { Head, Main, NextScript } from "next/document";
import flush from "styled-jsx/server";
import { ServerStyleSheet } from "styled-components";

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const initialProps = await Document.getInitialProps(ctx);
    return { ...initialProps };
  }

  render() {
    return (
      <html>
        <head
          dangerouslySetInnerHTML={{ __html: "<!-- jss-insertion-point -->" }}
        />
        <Head>
          <meta charSet="utf-8" />
          {/* Use minimum-scale=1 to enable GPU rasterization */}
          <meta
            name="viewport"
            content="minimum-scale=1, initial-scale=1, width=device-width, shrink-to-fit=no"
          />
          <link rel="manifest" href="static/manifest.json" />
          <link
            rel="stylesheet"
            href="https://fonts.googleapis.com/css?family=Roboto:300,400,500"
          />
          {this.props.styleTags}
        </Head>
        <body className="custom_class">
          <Main />
          <script src="static/js/dictate.js" />
          <script src="static/js/recorder.js" />
          <NextScript />
        </body>
      </html>
    );
  }
}

MyDocument.getInitialProps = ctx => {
  // Resolution order
  //
  // On the server:
  // 1. app.getInitialProps
  // 2. page.getInitialProps
  // 3. document.getInitialProps
  // 4. app.render
  // 5. page.render
  // 6. document.render
  //
  // On the server with error:
  // 1. document.getInitialProps
  // 2. app.render
  // 3. page.render
  // 4. document.render
  //
  // On the client
  // 1. app.getInitialProps
  // 2. page.getInitialProps
  // 3. app.render
  // 4. page.render

  // Render app and page and get the context of the page with collected side effects.
  let pageContext;

  const sheet = new ServerStyleSheet();

  const page = ctx.renderPage(Component => {
    const WrappedComponent = props => {
      pageContext = props.pageContext;
      return <Component {...props} />;
    };

    sheet.collectStyles(WrappedComponent);

    WrappedComponent.propTypes = {
      pageContext: PropTypes.object.isRequired
    };

    return WrappedComponent;
  });

  const styleTags = sheet.getStyleElement();

  let css;
  // It might be undefined, e.g. after an error.
  if (pageContext) {
    css = pageContext.sheetsRegistry.toString();
  }

  return {
    ...page,
    pageContext,
    styleTags,
    // Styles fragment is rendered after the app and page rendering finish.
    styles: (
      <Fragment>
        <style
          id="jss-server-side"
          // eslint-disable-next-line react/no-danger
          dangerouslySetInnerHTML={{ __html: css }}
        />
        {flush() || null}
      </Fragment>
    )
  };
};

export default MyDocument;
