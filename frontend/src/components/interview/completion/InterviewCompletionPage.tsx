import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Card, Statistic, Row, Col } from 'antd';
import { CheckCircleOutlined, ClockCircleOutlined, MessageOutlined, CodeOutlined } from '@ant-design/icons';

const InterviewCompletionPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    document.title = 'Interview Simulator | Results';
  }, []);

  // Hardcoded stats for now - will be replaced with real data later
  const stats = {
    totalDuration: '45:00',
    questionsAnswered: 12,
    technicalAccuracy: '85%',
    behavioralScore: '90%',
    codingScore: '75%',
    overallScore: '83%'
  };

  const handleReturnHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <CheckCircleOutlined style={{ fontSize: '64px', color: '#52c41a' }} />
          <h1 className="text-3xl font-bold mt-4 mb-2">Interview Completed!</h1>
          <p className="text-gray-600">Great job completing the interview simulation.</p>
        </div>

        <Row gutter={[24, 24]} className="mb-8">
          <Col xs={24} sm={12} md={8}>
            <Card>
              <Statistic
                title="Total Duration"
                value={stats.totalDuration}
                prefix={<ClockCircleOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card>
              <Statistic
                title="Questions Answered"
                value={stats.questionsAnswered}
                prefix={<MessageOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card>
              <Statistic
                title="Overall Score"
                value={stats.overallScore}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={[24, 24]} className="mb-12">
          <Col xs={24} sm={12}>
            <Card title="Technical Performance">
              <Statistic
                value={stats.technicalAccuracy}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12}>
            <Card title="Behavioral Performance">
              <Statistic
                value={stats.behavioralScore}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
        </Row>

        <div className="text-center">
          <Button
            type="primary"
            size="large"
            onClick={handleReturnHome}
            className="px-8"
          >
            Return to Home
          </Button>
        </div>
      </div>
    </div>
  );
};

export default InterviewCompletionPage; 