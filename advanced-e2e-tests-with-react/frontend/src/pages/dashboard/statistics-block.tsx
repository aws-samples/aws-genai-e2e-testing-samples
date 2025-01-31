/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

import {
  Container,
  Header,
  ColumnLayout,
  Box,
} from "@cloudscape-design/components";

export default function StatisticsBlock() {
  return (
    <Container header={<Header variant="h2">Statistics</Header>}>
      <ColumnLayout columns={4} variant="text-grid">
        <div>
          <Box variant="awsui-key-label">Items</Box>
          <div style={{ padding: "0.8rem 0", fontSize: "2.5rem" }}>42</div>
        </div>
        <div>
          <Box variant="awsui-key-label">Something Else</Box>
          <div style={{ padding: "0.8rem 0", fontSize: "2.5rem" }}>11</div>
        </div>
        <div>
          <Box variant="awsui-key-label">Another Item</Box>
          <div style={{ padding: "0.8rem 0", fontSize: "2.5rem" }}>18</div>
        </div>
        <div>
          <Box variant="awsui-key-label">Size</Box>
          <div style={{ padding: "0.8rem 0", fontSize: "2.5rem" }}>144</div>
        </div>
      </ColumnLayout>
    </Container>
  );
}
