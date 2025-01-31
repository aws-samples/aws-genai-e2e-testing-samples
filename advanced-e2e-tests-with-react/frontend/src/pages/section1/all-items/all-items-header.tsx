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
  Button,
  Header,
  HeaderProps,
  SpaceBetween,
} from "@cloudscape-design/components";
import RouterButton from "../../../components/wrappers/router-button";
import { useNavigate } from "react-router-dom";
import { Item } from "../../../common/types";

interface AllItemsPageHeaderProps extends HeaderProps {
  title?: string;
  createButtonText?: string;
  selectedItems: readonly Item[];
}

export function AllItemsPageHeader({
  title = "Items",
  ...props
}: AllItemsPageHeaderProps) {
  const navigate = useNavigate();

  return (
    <Header
      variant="awsui-h1-sticky"
      actions={
        <SpaceBetween size="xs" direction="horizontal">
          <Button iconName="refresh" />
          <RouterButton
            data-testid="header-btn-view-details"
            disabled={props.selectedItems.length !== 1}
            onClick={() =>
              navigate(`/section1/items/${props.selectedItems[0].itemId}`)
            }
          >
            View
          </RouterButton>
          <RouterButton
            data-testid="header-btn-view-details"
            disabled={props.selectedItems.length !== 1}
          >
            Delete
          </RouterButton>
          <RouterButton
            data-testid="header-btn-create"
            variant="primary"
            href="/section1/add"
          >
            Add Item
          </RouterButton>
        </SpaceBetween>
      }
      {...props}
    >
      {title}
    </Header>
  );
}
