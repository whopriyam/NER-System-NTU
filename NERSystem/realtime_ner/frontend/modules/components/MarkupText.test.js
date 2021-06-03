import React from "react";
import { shallow } from "enzyme";

import MarkupText from "./MarkupText";
import HighlightMark from "./HighlightMark";

describe("MarkupText", () => {
  it("should render correctly", () => {
    const wrapper = shallow(
      <MarkupText text="<CALL> malaysia one two </CALL> cleared for takeoff" />
    );
    expect(
      wrapper.containsAllMatchingElements([
        <HighlightMark type="CALL">malaysia one two</HighlightMark>,
        "cleared for takeoff"
      ])
    ).toBeTruthy();
  });
});
