/**
 * MongoDB User Seed Script
 * Adds 3 test users to the database
 * 
 * Usage: node scripts/seedUsers.js
 */

const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
require('dotenv').config();

const User = require('../models/User');

const users = [
  {
    name: 'Samy K Mottaya',
    email: 'samykmottaya@gmail.com',
    password: 'Danger!123',
    role: 'user'
  },
  {
    name: 'Muthu',
    email: 'abs@gmail.com',
    password: 'Danger!123',
    role: 'user'
  },
  {
    name: 'Test User',
    email: 'test@example.com',
    password: 'password123',
    role: 'user'
  }
];

const seedDatabase = async () => {
  try {
    // Connect to MongoDB
    const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017/skills-gap-analyzer';
    
    console.log('📦 Connecting to MongoDB...');
    console.log('📍 Database URI:', mongoUri);
    
    await mongoose.connect(mongoUri, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });

    console.log('✓ MongoDB connected successfully\n');

    // Clear existing users (optional - comment out if you want to keep them)
    // await User.deleteMany({});
    // console.log('✓ Cleared existing users\n');

    // Check for existing users
    const existingUsers = await User.find({
      email: { $in: users.map(u => u.email) }
    });

    if (existingUsers.length > 0) {
      console.log('⚠️  Found existing users:');
      existingUsers.forEach(u => {
        console.log(`   - ${u.email} (${u.name})`);
      });
      console.log('\n');
    }

    // Add new users
    console.log('📝 Adding users to database...\n');

    for (const userData of users) {
      const existingUser = await User.findOne({ email: userData.email });

      if (existingUser) {
        console.log(`⏭️  Skipping ${userData.email} (already exists)`);
        continue;
      }

      const user = await User.create({
        name: userData.name,
        email: userData.email,
        password: userData.password,
        role: userData.role
      });

      console.log(`✓ Created user: ${user.email}`);
      console.log(`  Name: ${user.name}`);
      console.log(`  Role: ${user.role}`);
      console.log(`  ID: ${user._id}\n`);
    }

    console.log('========================================');
    console.log('✓ Database seeding completed successfully!');
    console.log('========================================\n');

    // Display all users in database
    console.log('📋 All users in database:');
    const allUsers = await User.find({}, '-password');
    allUsers.forEach((user, index) => {
      console.log(`${index + 1}. ${user.email} (${user.name})`);
    });

    console.log('\n✓ You can now log in with any of these accounts');
    console.log('🔐 Test credentials:');
    users.forEach(u => {
      console.log(`   Email: ${u.email} | Password: ${u.password}`);
    });

  } catch (error) {
    console.error('✗ Error seeding database:', error.message);
    process.exit(1);
  } finally {
    await mongoose.connection.close();
    console.log('\n✓ Database connection closed');
    process.exit(0);
  }
};

// Run the seed script
seedDatabase();
