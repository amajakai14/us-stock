import React from 'react';
import {
  Container,
  Typography,
  Box,
  Alert,
  Button
} from '@mui/material';
import { Link } from 'react-router-dom';

const SchedulePage: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Data Collection Schedules
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Configure automated SEC data collection schedules for selected companies.
        </Typography>
      </Box>

      <Alert severity="info" sx={{ mb: 3 }}>
        This page will allow configuration of collection schedules with intervals, filing types, and execution history.
      </Alert>

      <Box sx={{ mb: 3 }}>
        <Button component={Link} to="/" variant="outlined">
          Back to Company List
        </Button>
      </Box>
    </Container>
  );
};

export default SchedulePage;