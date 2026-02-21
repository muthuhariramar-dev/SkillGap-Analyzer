/**
 * Authentication Integration Test
 * Tests MongoDB connection and authentication with the 3 test users
 * 
 * Usage: node scripts/testAuth.js
 */

const mongoose = require('mongoose');
const User = require('../models/User');
require('dotenv').config();

const testAccounts = [
  {
    email: 'samykmottaya@gmail.com',
    password: 'Danger!123',
    name: 'Samy K Mottaya'
  },
  {
    email: 'abs@gmail.com',
    password: 'Danger!123',
    name: 'Muthu'
  },
  {
    email: 'test@example.com',
    password: 'password123',
    name: 'Test User'
  }
];

const testAuthentication = async () => {
  try {
    const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017/skills-gap-analyzer';
    
    console.log('\n========================================');
    console.log('  MongoDB Authentication Test');
    console.log('========================================\n');

    console.log('📦 Connecting to MongoDB...');
    console.log('📍 Database URI:', mongoUri);
    console.log('');

    await mongoose.connect(mongoUri, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });

    console.log('✓ MongoDB connected successfully\n');

    // Test 1: Check if users exist in database
    console.log('========================================');
    console.log('Test 1: Checking for Users in Database');
    console.log('========================================\n');

    for (const account of testAccounts) {
      const user = await User.findOne({ email: account.email });
      
      if (user) {
        console.log(`✓ Found user: ${account.email}`);
        console.log(`  ID: ${user._id}`);
        console.log(`  Name: ${user.name}`);
        console.log(`  Role: ${user.role}`);
        console.log(`  Created: ${user.createdAt}\n`);
      } else {
        console.log(`✗ User not found: ${account.email}`);
        console.log(`  Run: npm run seed:users\n`);
      }
    }

    // Test 2: Test password verification
    console.log('========================================');
    console.log('Test 2: Password Verification');
    console.log('========================================\n');

    for (const account of testAccounts) {
      const user = await User.findOne({ email: account.email }).select('+password');
      
      if (user) {
        const isMatch = await user.matchPassword(account.password);
        
        if (isMatch) {
          console.log(`✓ ${account.email}`);
          console.log(`  Password matches!\n`);
        } else {
          console.log(`✗ ${account.email}`);
          console.log(`  Password DOES NOT match!\n`);
        }
      }
    }

    // Test 3: Test JWT Token Generation
    console.log('========================================');
    console.log('Test 3: JWT Token Generation');
    console.log('========================================\n');

    for (const account of testAccounts) {
      const user = await User.findOne({ email: account.email });
      
      if (user) {
        const token = user.getSignedJwtToken();
        console.log(`✓ ${account.email}`);
        console.log(`  Token generated (length: ${token.length})`);
        console.log(`  Token preview: ${token.substring(0, 20)}...\n`);
      }
    }

    // Test 4: Count total users
    console.log('========================================');
    console.log('Test 4: Database Statistics');
    console.log('========================================\n');

    const totalUsers = await User.countDocuments();
    const allUsers = await User.find({}, 'email name role createdAt');

    console.log(`Total users in database: ${totalUsers}\n`);

    if (allUsers.length > 0) {
      console.log('All users:');
      allUsers.forEach((user, index) => {
        console.log(`${index + 1}. ${user.email} (${user.name})`);
      });
      console.log('');
    }

    console.log('========================================');
    console.log('✓ All tests completed successfully!');
    console.log('========================================\n');

    console.log('📝 Next steps:');
    console.log('1. Start the backend server: npm run start:backend');
    console.log('2. Start the frontend: npm run start:frontend');
    console.log('3. Open http://localhost:3000 in your browser');
    console.log('4. Log in with one of the test accounts above\n');

  } catch (error) {
    console.error('✗ Test failed:', error.message);
    process.exit(1);
  } finally {
    await mongoose.connection.close();
    console.log('✓ Database connection closed');
    process.exit(0);
  }
};

// Run the test
testAuthentication();
