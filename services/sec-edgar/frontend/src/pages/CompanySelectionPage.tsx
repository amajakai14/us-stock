import React from 'react';
import {
  Container,
  Typography,
  Box,
  Alert,
  Button
} from '@mui/material';
import { Link } from 'react-router-dom';

const CompanySelectionPage: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Company Selections
        </Typography>
        <Typography variant="body1" color="text.secondary">
          View and manage companies selected for data collection.
        </Typography>
      </Box>

      <Alert severity="info" sx={{ mb: 3 }}>
        This page will show all selected companies with detailed information and bulk operations.
      </Alert>

      <Box sx={{ mb: 3 }}>
        <Button component={Link} to="/" variant="outlined">
          Back to Company List
        </Button>
      </Box>
    </Container>
  );
};

export default CompanySelectionPage;