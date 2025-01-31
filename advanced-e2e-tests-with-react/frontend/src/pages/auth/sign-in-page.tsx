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

import { useState } from 'react';
import { Box, Button, Container, FormField, Input, Header, SpaceBetween } from '@cloudscape-design/components';

function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSignIn = async (email: string, password: string) => {
    // Insert authentication logic here, like calling an API endpoint
    console.log('Signing in with', email, password);

    fetch('https://dummyjson.com/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: email,
          password: password,
          expiresInMins: 30, // optional, defaults to 60
        })
      })
      .then(res => {
        console.log(res.json());
        if (res.ok) {
          // If login is successful, redirect to the home page
          window.location.href = '/dashboard';
          return;
        }
      }).catch(() => {
        console.error("Error loggin in");
        setError('"Error loggin in. Invalid username or password.');
      });
  };

  const handleSubmit = async () => {
    setError('');

    // Basic client-side validation
    if (!email || !password) {
      setError('Please enter both username and password.');
      return;
    }
    try {
      // Call your sign-in logic here, passing email and password
      await handleSignIn(email, password);
    } catch (err) {
      setError('Invalid username or password.');
    }
  };

  return (
    <div style={styles.centeredContainer}>
        <div style={styles.containerWrapper}>
    <Container header={<Header variant="h2">Sign In</Header>}>
      <form onSubmit={(event) => event.preventDefault()}>
        <SpaceBetween direction="vertical" size="l">
          {error && <Box color="text-status-error">{error}</Box>}

          <FormField label="Username" errorText={!email && 'Username is required'}>
            <Input
              type="text"
              value={email}
              onChange={({ detail }) => setEmail(detail.value)}
              placeholder="Enter your username"
            />
          </FormField>

          <FormField label="Password" errorText={!password && 'Password is required'}>
            <Input
              type="text"
              value={password}
              onChange={({ detail }) => setPassword(detail.value)}
              placeholder="Enter your password"
            />
          </FormField>

          <Button variant="primary" onClick={handleSubmit}>
            Submit
          </Button>
        </SpaceBetween>
      </form>
    </Container>
    </div>
    </div>
  );
}

const styles = {
    centeredContainer: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
    } as React.CSSProperties,
    containerWrapper: {
      width: '400px',
    } as React.CSSProperties,
  };


export default SignInPage;
