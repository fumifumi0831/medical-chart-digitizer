// Example test file using Jest and React Testing Library
// When implementing tests, uncomment and complete the code below

/*
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ImageUploader from '../ImageUploader';
import * as api from '../../lib/api';

// Mock the API module
jest.mock('../../lib/api');

describe('ImageUploader', () => {
  const mockOnUploadSuccess = jest.fn();
  const mockOnUploadError = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('renders the uploader component correctly', () => {
    render(
      <ImageUploader 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    // Check if the component renders properly
    expect(screen.getByText(/クリックしてファイルを選択/)).toBeInTheDocument();
    expect(screen.getByText(/JPEG または PNG, 最大10MB/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /画像を選択/ })).toBeInTheDocument();
  });
  
  it('handles successful file upload', async () => {
    // Mock the uploadChart function to return a successful response
    const mockChartId = '12345-abcde';
    (api.uploadChart as jest.Mock).mockResolvedValue({ chart_id: mockChartId });
    
    render(
      <ImageUploader 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    // Create a test file
    const file = new File(['test image content'], 'test.jpg', { type: 'image/jpeg' });
    
    // Trigger file selection
    const input = screen.getByRole('button', { name: /画像を選択/ });
    fireEvent.click(input);
    
    // TODO: Complete this test by simulating file drop
    
    // Wait for the upload to complete
    await waitFor(() => {
      expect(api.uploadChart).toHaveBeenCalledWith(file);
      expect(mockOnUploadSuccess).toHaveBeenCalledWith(mockChartId);
    });
  });
  
  it('shows error for invalid file type', async () => {
    render(
      <ImageUploader 
        onUploadSuccess={mockOnUploadSuccess} 
        onUploadError={mockOnUploadError} 
      />
    );
    
    // Create an invalid file type
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    
    // TODO: Complete this test by simulating file drop with invalid type
    
    // Check if error handler was called
    await waitFor(() => {
      expect(mockOnUploadError).toHaveBeenCalledWith('ファイル形式はJPEGまたはPNGのみです。');
    });
  });
});
*/
