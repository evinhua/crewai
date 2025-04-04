import React, { useState } from 'react';
import { Container, Row, Col, Form, Button, Card, Spinner, Alert } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { generateContent } from './services/api';

function App() {
  const [formData, setFormData] = useState({
    contentType: 'blog',
    topic: '',
    targetAudience: '',
    tone: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [step, setStep] = useState(1);
  const [progress, setProgress] = useState({
    research: false,
    writing: false,
    editing: false,
    seo: false
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      // Update progress states for visual feedback
      setProgress({ research: true, writing: false, editing: false, seo: false });
      
      // In a production environment, this would call the actual API
      // For demo purposes, we'll use the mock function
      // Uncomment the following lines to use the actual API
      /*
      const response = await generateContent({
        contentType: formData.contentType,
        topic: formData.topic,
        targetAudience: formData.targetAudience,
        tone: formData.tone
      });
      setResult(response.content);
      */
      
      // Mock implementation with timeouts to simulate the process
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProgress({ research: true, writing: true, editing: false, seo: false });
      
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProgress({ research: true, writing: true, editing: true, seo: false });
      
      await new Promise(resolve => setTimeout(resolve, 2000));
      setProgress({ research: true, writing: true, editing: true, seo: true });
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Generate mock result based on input
      const mockResult = generateMockResult(formData);
      setResult(mockResult);
      setStep(2);
    } catch (err) {
      setError('An error occurred while generating content. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
      setProgress({
        research: false,
        writing: false,
        editing: false,
        seo: false
      });
    }
  };

  const generateMockResult = (data) => {
    return `# ${data.contentType.charAt(0).toUpperCase() + data.contentType.slice(1)}: ${data.topic}

Target Audience: ${data.targetAudience}
Tone: ${data.tone}
Created: ${new Date().toLocaleString()}

---

## Introduction

This is a sample ${data.contentType} about ${data.topic} written in a ${data.tone} tone for ${data.targetAudience}.

## Key Points

1. First important point about ${data.topic}
2. Second important consideration
3. Interesting perspective that engages ${data.targetAudience}

## Main Content

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam eget felis eget urna ultricies 
tincidunt. Vestibulum tincidunt est vitae ultrices accumsan. Aliquam ornare lacus adipiscing, 
posuere lectus et, fringilla augue.

## Conclusion

To summarize the key points about ${data.topic} that would interest ${data.targetAudience}...

## SEO Recommendations

**Keywords:** ${data.topic.toLowerCase()}, ${data.topic.toLowerCase()} tips, ${data.topic.toLowerCase()} for ${data.targetAudience.toLowerCase()}

**Meta Description:** Learn everything about ${data.topic} in this comprehensive guide written specifically for ${data.targetAudience}.
`;
  };

  const resetForm = () => {
    setStep(1);
    setResult(null);
  };
  
  const handleDownload = () => {
    if (!result) return;
    
    const filename = `${formData.contentType}_${formData.topic.replace(/\s+/g, '_').toLowerCase()}_${new Date().toISOString().slice(0, 10)}.md`;
    const blob = new Blob([result], { type: 'text/markdown' });
    const href = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = href;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    
    document.body.removeChild(link);
    URL.revokeObjectURL(href);
  };

  return (
    <Container className="py-5">
      <Row className="mb-5">
        <Col>
          <h1 className="text-center">CrewAI Content Creation System</h1>
          <p className="text-center lead">
            Generate high-quality content with a team of AI agents working together
          </p>
        </Col>
      </Row>

      {step === 1 ? (
        <Row className="justify-content-center">
          <Col md={8}>
            <Card className="shadow">
              <Card.Header as="h5">Content Creation Form</Card.Header>
              <Card.Body>
                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label>Content Type</Form.Label>
                    <Form.Select 
                      name="contentType" 
                      value={formData.contentType}
                      onChange={handleChange}
                      required
                    >
                      <option value="blog">Blog Post</option>
                      <option value="social">Social Media</option>
                      <option value="email">Email</option>
                    </Form.Select>
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Topic</Form.Label>
                    <Form.Control
                      type="text"
                      name="topic"
                      value={formData.topic}
                      onChange={handleChange}
                      placeholder="Enter the topic for your content"
                      required
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Target Audience</Form.Label>
                    <Form.Control
                      type="text"
                      name="targetAudience"
                      value={formData.targetAudience}
                      onChange={handleChange}
                      placeholder="Who is the target audience?"
                      required
                    />
                  </Form.Group>

                  <Form.Group className="mb-3">
                    <Form.Label>Tone</Form.Label>
                    <Form.Control
                      type="text"
                      name="tone"
                      value={formData.tone}
                      onChange={handleChange}
                      placeholder="e.g., professional, casual, humorous"
                      required
                    />
                  </Form.Group>

                  {error && <Alert variant="danger">{error}</Alert>}

                  <div className="d-grid gap-2">
                    <Button 
                      variant="primary" 
                      type="submit" 
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <Spinner
                            as="span"
                            animation="border"
                            size="sm"
                            role="status"
                            aria-hidden="true"
                            className="me-2"
                          />
                          Generating Content...
                        </>
                      ) : 'Generate Content'}
                    </Button>
                  </div>
                </Form>

                {loading && (
                  <div className="mt-4">
                    <h6>Progress:</h6>
                    <div className="progress-tracker">
                      <div className={`progress-step ${progress.research ? 'active' : ''}`}>
                        <div className="step-icon">1</div>
                        <div className="step-label">Research</div>
                      </div>
                      <div className={`progress-step ${progress.writing ? 'active' : ''}`}>
                        <div className="step-icon">2</div>
                        <div className="step-label">Writing</div>
                      </div>
                      <div className={`progress-step ${progress.editing ? 'active' : ''}`}>
                        <div className="step-icon">3</div>
                        <div className="step-label">Editing</div>
                      </div>
                      <div className={`progress-step ${progress.seo ? 'active' : ''}`}>
                        <div className="step-icon">4</div>
                        <div className="step-label">SEO</div>
                      </div>
                    </div>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      ) : (
        <Row>
          <Col md={4} className="mb-4">
            <Card className="shadow h-100">
              <Card.Header as="h5">Content Details</Card.Header>
              <Card.Body>
                <p><strong>Content Type:</strong> {formData.contentType}</p>
                <p><strong>Topic:</strong> {formData.topic}</p>
                <p><strong>Target Audience:</strong> {formData.targetAudience}</p>
                <p><strong>Tone:</strong> {formData.tone}</p>
                <div className="d-grid gap-2 mt-4">
                  <Button variant="primary" onClick={resetForm}>Create New Content</Button>
                  <Button variant="outline-secondary" onClick={handleDownload}>Download as Markdown</Button>
                </div>
              </Card.Body>
            </Card>
          </Col>
          <Col md={8}>
            <Card className="shadow">
              <Card.Header as="h5">Generated Content</Card.Header>
              <Card.Body className="content-preview">
                <ReactMarkdown>{result}</ReactMarkdown>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )}

      <footer className="mt-5 text-center text-muted">
        <p>Powered by CrewAI - A collaborative AI content generation system</p>
      </footer>
    </Container>
  );
}

export default App;
