import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Button, Form, Table } from 'react-bootstrap';
import axios from 'axios';

function Dashboard() {
  // States for Company
  const [companies, setCompanies] = useState([]);
  const [companyName, setCompanyName] = useState('');
  const [companyAddress, setCompanyAddress] = useState('');
  const [companyEmail, setCompanyEmail] = useState('');

  // States for Department
  const [departments, setDepartments] = useState([]);
  const [departmentName, setDepartmentName] = useState('');
  const [departmentDescription, setDepartmentDescription] = useState('');
  const [selectedCompanyId, setSelectedCompanyId] = useState('');

  // Fetch companies and departments on component mount
  useEffect(() => {
    fetchCompanies();
    fetchDepartments();
  }, []);

  const fetchCompanies = () => {
    axios.get('/api/company/')
      .then(response => {
        setCompanies(response.data);
      })
      .catch(error => console.error('There was an error fetching companies!', error));
  };

  const fetchDepartments = () => {
    axios.get('/api/department/')
      .then(response => {
        setDepartments(response.data);
      })
      .catch(error => console.error('There was an error fetching departments!', error));
  };

  const handleAddCompany = () => {
    axios.post('/api/company/', { name: companyName, address: companyAddress, email: companyEmail })
      .then(() => {
        fetchCompanies();
        setCompanyName('');
        setCompanyAddress('');
        setCompanyEmail('');
      })
      .catch(error => console.error('There was an error adding the company!', error));
  };

  const handleDeleteCompany = (id) => {
    axios.delete(`/api/company/${id}/`)
      .then(() => fetchCompanies())
      .catch(error => console.error('There was an error deleting the company!', error));
  };

  const handleAddDepartment = () => {
    axios.post('/api/department/', { name: departmentName, description: departmentDescription, company: selectedCompanyId })
      .then(() => {
        fetchDepartments();
        setDepartmentName('');
        setDepartmentDescription('');
      })
      .catch(error => console.error('There was an error adding the department!', error));
  };

  const handleDeleteDepartment = (id) => {
    axios.delete(`/api/department/${id}/`)
      .then(() => fetchDepartments())
      .catch(error => console.error('There was an error deleting the department!', error));
  };

  return (
    <Container>
      {/* Company Management */}
      <Row className="mb-4">
        <Col>
          <h2>Manage Companies</h2>
          <Form className="mb-3">
            <Form.Group controlId="formCompanyName" className="mb-2">
              <Form.Label>Company Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter company name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
              />
            </Form.Group>
            <Form.Group controlId="formCompanyAddress" className="mb-2">
              <Form.Label>Address</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter address"
                value={companyAddress}
                onChange={(e) => setCompanyAddress(e.target.value)}
              />
            </Form.Group>
            <Form.Group controlId="formCompanyEmail" className="mb-2">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                value={companyEmail}
                onChange={(e) => setCompanyEmail(e.target.value)}
              />
            </Form.Group>
            <Button variant="primary" onClick={handleAddCompany}>Add Company</Button>
          </Form>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Name</th>
                <th>Address</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {companies.map(company => (
                <tr key={company.id}>
                  <td>{company.name}</td>
                  <td>{company.address}</td>
                  <td>{company.email}</td>
                  <td>
                    <Button variant="danger" onClick={() => handleDeleteCompany(company.id)}>Delete</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>

      {/* Department Management */}
      <Row className="mt-4">
        <Col>
          <h2>Manage Departments</h2>
          <Form className="mb-3">
            <Form.Group controlId="formDepartmentName" className="mb-2">
              <Form.Label>Department Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter department name"
                value={departmentName}
                onChange={(e) => setDepartmentName(e.target.value)}
              />
            </Form.Group>
            <Form.Group controlId="formDepartmentDescription" className="mb-2">
              <Form.Label>Description</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter description"
                value={departmentDescription}
                onChange={(e) => setDepartmentDescription(e.target.value)}
              />
            </Form.Group>
            <Form.Group controlId="formCompanySelect" className="mb-2">
              <Form.Label>Select Company</Form.Label>
              <Form.Control
                as="select"
                value={selectedCompanyId}
                onChange={(e) => setSelectedCompanyId(e.target.value)}
              >
                <option value="">Select a company...</option>
                {companies.map(company => (
                  <option key={company.id} value={company.id}>{company.name}</option>
                ))}
              </Form.Control>
            </Form.Group>
            <Button variant="primary" onClick={handleAddDepartment}>Add Department</Button>
          </Form>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Company</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {departments.map(department => (
                <tr key={department.id}>
                  <td>{department.name}</td>
                  <td>{department.description}</td>
                  <td>{companies.find(company => company.id === department.company)?.name}</td>
                  <td>
                    <Button variant="danger" onClick={() => handleDeleteDepartment(department.id)}>Delete</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard;
