import styled from "styled-components";
import randomColor from "randomcolor";

const RANDOM_COLOR_SEED = 250;

const colorMemo = {

};

const randomColors = randomColor({
  luminosity: "bright",
  seed: RANDOM_COLOR_SEED,
  count: 1000
});
let randomColorIdx = 0;
const colorOfType = type => {
  if (colorMemo[type]) {
    return colorMemo[type];
  } else {
    colorMemo[type] = randomColors[randomColorIdx];
    randomColorIdx += 10;
    return colorMemo[type];
  }
};
/*
add widget component, show colour memo pass from this component to widget , make changes and update via props change random colour to state variables
*/

const HighlightMark = styled.mark`
  display: inline-block;
  line-height: 1;
  background-color: transparent;
  color: inherit;
`;

const HighlightMarkBox = styled(HighlightMark)`
  border: 2px solid ${props => colorOfType(props.type)};
  border-radius: 8px;
  padding-left: 0.35em;

  &::after {
    display: inline-block;
    box-sizing: border-box;
    line-height: 1;
    padding: 0.25em 0.35em;
    margin-left: 0.35em;
    color: #fff;
    font-size: 0.95em;
    font-weight: bold;
    background-color: ${props => colorOfType(props.type)};
    content: "${props => props.type}";
  }
`;

const HighlightMarkUnderline = styled(HighlightMark)`
  padding: 0 9em 0.15em 0.15em;
  position: relative;
  cursor: help;
  border-bottom: 3px solid ${props => colorOfType(props.type)};

  &::after {
    box-sizing: border-box;
    line-height: 1;
    display: inline-block;
    font-size: 0.75em;
    font-weight: bold;
    text-transform: uppercase;
    position: absolute;
    bottom: -1.5em;
    left: 0;
    transition: opacity 0.25s ease;
    color: ${props => colorOfType(props.type)};
    content: "${props => props.type}";
    opacity: 1;
  }

  &:hover::after{
    opacity: 1;
  }
`;

export { HighlightMarkBox, HighlightMarkUnderline };
