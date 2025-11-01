import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import CompanyListPage from './pages/CompanyListPage';
import CompanySelectionPage from './pages/CompanySelectionPage';
import SchedulePage from './pages/SchedulePage';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ flexGrow: 1 }}>
          {/* Header */}
          <Box sx={{ bgcolor: 'primary.main', color: 'white', py: 2 }}>
            <Container maxWidth="lg">
              <Typography variant="h4" component="h1">
                US Stock Data Collection
              </Typography>
              <Typography variant="subtitle1">
                Discover, select, and track SEC data for US stocks
              </Typography>
            </Container>
          </Box>

          {/* Main Content */}
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Routes>
              <Route path="/" element={<CompanyListPage />} />
              <Route path="/selections" element={<CompanySelectionPage />} />
              <Route path="/schedules" element={<SchedulePage />} />
            </Routes>
          </Container>

          {/* Footer */}
          <Box sx={{ bgcolor: 'grey.200', py: 2, mt: 'auto' }}>
            <Container maxWidth="lg">
              <Typography variant="body2" color="text.secondary" align="center">
                © 2024 US Stock Data Collection System
              </Typography>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;