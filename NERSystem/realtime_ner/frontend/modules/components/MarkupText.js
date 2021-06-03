import React from "react";
import styled from "styled-components";
import Typography from "@material-ui/core/Typography";
import { HighlightMarkUnderline as HighlightMark } from "./HighlightMark";

const OPENING_TAG_RE = /<([a-zA-Z\-]+)>/;
const CLOSING_TAG_RE = /<\/([a-zA-Z\-]+)>/;

const markupToSegments = markupText => {
  const segments = [];
  const tokens = markupText.split(" ");
  let curSegment = { tokens: [] };

  tokens.forEach(token => {
    const openingTagMatch = token.match(OPENING_TAG_RE);
    const closingTagMatch = token.match(CLOSING_TAG_RE);

    if (openingTagMatch) {
      segments.push(curSegment);
      curSegment = { tokens: [], tag: openingTagMatch[1] };
    } else if (closingTagMatch) {
      segments.push(curSegment);
      curSegment = { tokens: [] };
    } else {
      curSegment["tokens"].push(token);
    }
  });

  if (curSegment["tokens"].length !== 0) {
    segments.push(curSegment);
  }

  return segments;
};

const MarkupTypography = styled(Typography).attrs({
  variant: "body1"
})`
  line-height: 2.5;
`;

const MarkupText = ({ text }) => {
  const renderSegments = [];
  markupToSegments(text).forEach((segment, idx) => {
    if (segment.hasOwnProperty("tag")) {
      renderSegments.push(
        <HighlightMark type={segment.tag} key={idx}>
          {segment.tokens.join(" ")}
        </HighlightMark>
      );
    } else {
      renderSegments.push(segment.tokens.join(" "));
    }
    renderSegments.push(" ");
  });
  return <MarkupTypography>{renderSegments}</MarkupTypography>;
};

export default MarkupText;
