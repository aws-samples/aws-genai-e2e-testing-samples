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
  BreadcrumbGroup,
  Button,
  Container,
  ContentLayout,
  Form,
  FormField,
  Header,
  Input,
  SpaceBetween,
} from "@cloudscape-design/components";
import { useState } from "react";
import { APP_NAME } from "../../../common/constants";
import { useOnFollow } from "../../../common/hooks/use-on-follow";
import BaseAppLayout from "../../../components/base-app-layout";
import RouterButton from "../../../components/wrappers/router-button";
import { Item } from "../../../common/types";
import { Utils } from "../../../common/utils";
import { useItemsDispatch } from "../../../context/ItemsContext";
import { useNavigate } from "react-router-dom";

export default function AddItemPage() {
  const dispatch = useItemsDispatch();
  const onFollow = useOnFollow();
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);
  const [globalError, setGlobalError] = useState<string | undefined>(undefined);
  const [name, setName] = useState<string>("");

  const submitForm = async () => {
    setSubmitting(true);
    if (!name) {
      setGlobalError("Item name is required!");
    }else {
      await Utils.promiseSetTimeout(100)
      dispatch({ type: 'CREATE', payload: { name } as Item });
      setName("");
    }
    setSubmitting(false);
    // navigate to all items page
    navigate("/section1");
  };
  return (
    <BaseAppLayout
      breadcrumbs={
        <BreadcrumbGroup
          onFollow={onFollow}
          items={[
            {
              text: APP_NAME,
              href: "/",
            },
            {
              text: "Items",
              href: "/section1",
            },
            {
              text: "Add Item",
              href: "/section1/add",
            },
          ]}
          expandAriaLabel="Show path"
          ariaLabel="Breadcrumbs"
        />
      }
      content={
        <ContentLayout
          header={
            <Header variant="h1" description="Add a new item to the list">
              Add Item
            </Header>
          }
        >
          <form onSubmit={(event) => event.preventDefault()}>
            <Form
              actions={
                <SpaceBetween direction="horizontal" size="xs">
                  <RouterButton variant="link" href="/section1">
                    Cancel
                  </RouterButton>
                  <Button
                    data-testid="create"
                    variant="primary"
                    onClick={submitForm}
                    disabled={submitting}
                  >
                    Add Item
                  </Button>
                </SpaceBetween>
              }
              errorText={globalError}
            >
              <Container
                header={<Header variant="h2">Item Configuration</Header>}
              >
                <SpaceBetween size="l">
                  <FormField label="Item Name">
                    <Input
                      placeholder="My Item"
                      disabled={submitting}
                      value={name}
                      onChange={(event) => setName(event.detail.value)}
                    />
                  </FormField>
                </SpaceBetween>
              </Container>
            </Form>
          </form>
        </ContentLayout>
      }
    />
  );
}
