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

import { Header, SpaceBetween } from "@cloudscape-design/components";
import RouterButton from "../../components/wrappers/router-button";
import RouterButtonDropdown from "../../components/wrappers/router-button-dropdown";

export default function DashboardHeader() {
  const downloadImage = async () => {
    const imageUrl =
      'https://images.pexels.com/photos/1563356/pexels-photo-1563356.jpeg?cs=srgb&dl=pexels-thatguycraig000-1563356.jpg&fm=jpg&w=640&h=427';

    try {
      const response = await fetch(imageUrl);

      if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.statusText}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      // Create a link and programmatically click it to trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = 'computer-use-demo-picture.jpg'; // Set the filename
      document.body.appendChild(link);
      link.click();

      // Cleanup
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading the image:', error);
    }
  };

  return (
    <Header
      variant="h1"
      actions={
        <SpaceBetween direction="horizontal" size="xs">
          <RouterButton onClick={downloadImage}>Download Image</RouterButton>
          <RouterButton href="/section1">View Items</RouterButton>
          <RouterButtonDropdown
            items={[
              {
                id: "add-data",
                text: "Add Item",
                href: "/section1/add",
              },
            ]}
          >
            Add data
          </RouterButtonDropdown>
        </SpaceBetween>
      }
    >
      Dashboard
    </Header>
  );
}
