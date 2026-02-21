"""
Market Analysis Model - Job Market Trend Analysis

This module implements comprehensive job market analysis functionality that
tracks trends, predicts demand, and provides insights for career planning.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

# ML imports
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.cluster import KMeans

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrendDirection(Enum):
    """Market trend directions"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


class MarketSegment(Enum):
    """Market segments for analysis"""
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    CONSULTING = "consulting"


@dataclass
class JobPosting:
    """Represents a job posting with market data"""
    job_id: str
    title: str
    company: str
    location: str
    salary_range: Tuple[int, int]
    required_skills: List[str]
    experience_level: str
    posting_date: datetime
    market_segment: MarketSegment
    remote_work: bool


@dataclass
class MarketTrend:
    """Represents a market trend analysis"""
    skill_name: str
    trend_direction: TrendDirection
    growth_rate: float
    demand_score: float
    salary_trend: float
    market_share: float
    prediction_confidence: float


@dataclass
class RegionalMarket:
    """Represents regional market data"""
    region: str
    total_postings: int
    average_salary: float
    top_skills: List[str]
    growth_rate: float
    competition_level: float


class MarketAnalyzer:
    """
    Job Market Analysis System
    
    This class implements ML-based market analysis for job trends,
    salary predictions, and regional market insights.
    """
    
    def __init__(self):
        """Initialize the market analysis system"""
        self.logger = logging.getLogger(__name__)
        
        # ML models
        self.trend_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.salary_predictor = RandomForestRegressor(n_estimators=100, random_state=42)
        self.demand_classifier = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.market_clusterer = KMeans(n_clusters=5, random_state=42)
        
        # Data preprocessing
        self.scaler = StandardScaler()
        self.skill_encoder = LabelEncoder()
        self.region_encoder = LabelEncoder()
        
        # Market data storage
        self.job_postings = []
        self.market_trends = {}
        self.regional_markets = {}
        self.skill_demand_history = {}
        
        # Configuration
        self.analysis_config = {
            "trend_window_months": 12,
            "prediction_horizon_months": 6,
            "min_postings_for_analysis": 50,
            "salary_adjustment_inflation": 0.03
        }
        
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample market data for demonstration"""
        sample_postings = [
            JobPosting(
                job_id="job_001",
                title="Data Scientist",
                company="TechCorp",
                location="San Francisco",
                salary_range=(120000, 180000),
                required_skills=["Python", "Machine Learning", "SQL", "Statistics"],
                experience_level="Senior",
                posting_date=datetime.now() - timedelta(days=30),
                market_segment=MarketSegment.TECHNOLOGY,
                remote_work=True
            ),
            JobPosting(
                job_id="job_002",
                title="ML Engineer",
                company="DataTech",
                location="New York",
                salary_range=(130000, 170000),
                required_skills=["Python", "Deep Learning", "Cloud Computing", "DevOps"],
                experience_level="Mid-level",
                posting_date=datetime.now() - timedelta(days=15),
                market_segment=MarketSegment.TECHNOLOGY,
                remote_work=True
            ),
            JobPosting(
                job_id="job_003",
                title="Data Analyst",
                company="FinanceCorp",
                location="Chicago",
                salary_range=(70000, 90000),
                required_skills=["SQL", "Excel", "Tableau", "Business Analysis"],
                experience_level="Junior",
                posting_date=datetime.now() - timedelta(days=45),
                market_segment=MarketSegment.FINANCE,
                remote_work=False
            )
        ]
        
        self.job_postings = sample_postings
        self._process_market_data()
    
    def _process_market_data(self):
        """Process raw job posting data for analysis"""
        try:
            if not self.job_postings:
                return
            
            # Convert to DataFrame for analysis
            df_data = []
            for posting in self.job_postings:
                for skill in posting.required_skills:
                    df_data.append({
                        'job_id': posting.job_id,
                        'title': posting.title,
                        'company': posting.company,
                        'location': posting.location,
                        'min_salary': posting.salary_range[0],
                        'max_salary': posting.salary_range[1],
                        'avg_salary': sum(posting.salary_range) / 2,
                        'skill': skill,
                        'experience_level': posting.experience_level,
                        'posting_date': posting.posting_date,
                        'market_segment': posting.market_segment.value,
                        'remote_work': posting.remote_work
                    })
            
            self.market_df = pd.DataFrame(df_data)
            
            # Analyze skill demand
            self._analyze_skill_demand()
            
            # Analyze regional markets
            self._analyze_regional_markets()
            
            # Calculate market trends
            self._calculate_market_trends()
            
        except Exception as e:
            self.logger.error(f"Error processing market data: {e}")
    
    def _analyze_skill_demand(self):
        """Analyze demand for different skills"""
        try:
            if self.market_df.empty:
                return
            
            # Skill demand analysis
            skill_demand = self.market_df.groupby('skill').agg({
                'job_id': 'count',
                'avg_salary': 'mean',
                'min_salary': 'min',
                'max_salary': 'max'
            }).rename(columns={'job_id': 'posting_count'})
            
            # Calculate demand scores
            total_postings = len(self.market_df)
            skill_demand['demand_score'] = skill_demand['posting_count'] / total_postings
            
            # Sort by demand
            skill_demand = skill_demand.sort_values('posting_count', ascending=False)
            
            self.skill_demand_analysis = skill_demand
            
        except Exception as e:
            self.logger.error(f"Error analyzing skill demand: {e}")
    
    def _analyze_regional_markets(self):
        """Analyze market data by region"""
        try:
            if self.market_df.empty:
                return
            
            # Regional analysis
            regional_data = self.market_df.groupby('location').agg({
                'job_id': 'count',
                'avg_salary': 'mean',
                'skill': lambda x: list(x.unique())
            }).rename(columns={'job_id': 'total_postings'})
            
            # Calculate competition level (inverse of average salary)
            max_salary = regional_data['avg_salary'].max()
            regional_data['competition_level'] = 1 - (regional_data['avg_salary'] / max_salary)
            
            # Calculate growth rate (mock data for demonstration)
            regional_data['growth_rate'] = np.random.uniform(0.02, 0.15, len(regional_data))
            
            self.regional_analysis = regional_data
            
        except Exception as e:
            self.logger.error(f"Error analyzing regional markets: {e}")
    
    def _calculate_market_trends(self):
        """Calculate market trends for skills and roles"""
        try:
            if self.market_df.empty:
                return
            
            trends = {}
            
            # Calculate trends for each skill
            for skill in self.market_df['skill'].unique():
                skill_data = self.market_df[self.market_df['skill'] == skill]
                
                # Mock trend calculation (in real implementation, would use historical data)
                posting_trend = np.random.uniform(-0.1, 0.3)
                salary_trend = np.random.uniform(-0.05, 0.15)
                
                # Determine trend direction
                if posting_trend > 0.1:
                    direction = TrendDirection.INCREASING
                elif posting_trend < -0.1:
                    direction = TrendDirection.DECREASING
                elif abs(posting_trend) < 0.05:
                    direction = TrendDirection.STABLE
                else:
                    direction = TrendDirection.VOLATILE
                
                # Calculate demand score
                demand_score = len(skill_data) / len(self.market_df)
                
                trend = MarketTrend(
                    skill_name=skill,
                    trend_direction=direction,
                    growth_rate=posting_trend,
                    demand_score=demand_score,
                    salary_trend=salary_trend,
                    market_share=demand_score,
                    prediction_confidence=np.random.uniform(0.7, 0.95)
                )
                
                trends[skill] = trend
            
            self.market_trends = trends
            
        except Exception as e:
            self.logger.error(f"Error calculating market trends: {e}")
    
    def get_skill_demand_analysis(self, skill_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get demand analysis for specific skill or all skills
        
        Args:
            skill_name: Specific skill to analyze (optional)
            
        Returns:
            Dictionary with demand analysis
        """
        try:
            if not hasattr(self, 'skill_demand_analysis') or self.skill_demand_analysis.empty:
                return {"error": "No market data available"}
            
            if skill_name:
                if skill_name not in self.skill_demand_analysis.index:
                    return {"error": f"Skill '{skill_name}' not found in market data"}
                
                skill_data = self.skill_demand_analysis.loc[skill_name]
                return {
                    "skill": skill_name,
                    "posting_count": int(skill_data['posting_count']),
                    "average_salary": float(skill_data['avg_salary']),
                    "salary_range": (int(skill_data['min_salary']), int(skill_data['max_salary'])),
                    "demand_score": float(skill_data['demand_score']),
                    "market_rank": int(self.skill_demand_analysis.index.get_loc(skill_name) + 1)
                }
            else:
                # Return top skills
                top_skills = self.skill_demand_analysis.head(10)
                return {
                    "total_skills_analyzed": len(self.skill_demand_analysis),
                    "top_skills": [
                        {
                            "skill": skill,
                            "posting_count": int(row['posting_count']),
                            "average_salary": float(row['avg_salary']),
                            "demand_score": float(row['demand_score'])
                        }
                        for skill, row in top_skills.iterrows()
                    ]
                }
                
        except Exception as e:
            self.logger.error(f"Error getting skill demand analysis: {e}")
            return {"error": str(e)}
    
    def get_regional_market_insights(self, region: Optional[str] = None) -> Dict[str, Any]:
        """
        Get regional market insights
        
        Args:
            region: Specific region to analyze (optional)
            
        Returns:
            Dictionary with regional insights
        """
        try:
            if not hasattr(self, 'regional_analysis') or self.regional_analysis.empty:
                return {"error": "No regional data available"}
            
            if region:
                if region not in self.regional_analysis.index:
                    return {"error": f"Region '{region}' not found in data"}
                
                region_data = self.regional_analysis.loc[region]
                return {
                    "region": region,
                    "total_postings": int(region_data['total_postings']),
                    "average_salary": float(region_data['avg_salary']),
                    "top_skills": region_data['skill'][:5],  # Top 5 skills
                    "growth_rate": float(region_data['growth_rate']),
                    "competition_level": float(region_data['competition_level'])
                }
            else:
                # Return all regions
                return {
                    "total_regions": len(self.regional_analysis),
                    "regions": [
                        {
                            "region": region,
                            "total_postings": int(row['total_postings']),
                            "average_salary": float(row['avg_salary']),
                            "growth_rate": float(row['growth_rate']),
                            "competition_level": float(row['competition_level'])
                        }
                        for region, row in self.regional_analysis.iterrows()
                    ]
                }
                
        except Exception as e:
            self.logger.error(f"Error getting regional market insights: {e}")
            return {"error": str(e)}
    
    def predict_salary_trends(self, skill_name: str, months_ahead: int = 6) -> Dict[str, Any]:
        """
        Predict salary trends for a specific skill
        
        Args:
            skill_name: Skill to predict trends for
            months_ahead: Number of months to predict
            
        Returns:
            Dictionary with salary trend predictions
        """
        try:
            if skill_name not in self.market_trends:
                return {"error": f"No trend data available for skill '{skill_name}'"}
            
            trend = self.market_trends[skill_name]
            
            # Calculate predicted salary growth
            monthly_growth = trend.salary_trend / 12
            predicted_growth = (1 + monthly_growth) ** months_ahead - 1
            
            # Get current salary data
            current_analysis = self.get_skill_demand_analysis(skill_name)
            if "error" in current_analysis:
                return current_analysis
            
            current_avg_salary = current_analysis["average_salary"]
            predicted_salary = current_avg_salary * (1 + predicted_growth)
            
            return {
                "skill": skill_name,
                "current_average_salary": current_avg_salary,
                "predicted_salary": predicted_salary,
                "predicted_growth_rate": predicted_growth,
                "prediction_horizon_months": months_ahead,
                "confidence": trend.prediction_confidence,
                "trend_direction": trend.trend_direction.value
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting salary trends: {e}")
            return {"error": str(e)}
    
    def analyze_market_competition(self, skill_set: List[str]) -> Dict[str, Any]:
        """
        Analyze market competition for a set of skills
        
        Args:
            skill_set: List of skills to analyze
            
        Returns:
            Dictionary with competition analysis
        """
        try:
            if not skill_set:
                return {"error": "No skills provided for analysis"}
            
            # Get demand data for each skill
            skill_data = {}
            total_demand = 0
            
            for skill in skill_set:
                analysis = self.get_skill_demand_analysis(skill)
                if "error" not in analysis:
                    skill_data[skill] = analysis
                    total_demand += analysis["demand_score"]
            
            if not skill_data:
                return {"error": "No market data found for provided skills"}
            
            # Calculate competition metrics
            avg_demand_score = total_demand / len(skill_set)
            avg_salary = np.mean([data["average_salary"] for data in skill_data.values()])
            
            # Determine competition level
            if avg_demand_score > 0.1:
                competition_level = "High"
            elif avg_demand_score > 0.05:
                competition_level = "Medium"
            else:
                competition_level = "Low"
            
            # Find skill gaps (skills with low demand)
            low_demand_skills = [
                skill for skill, data in skill_data.items()
                if data["demand_score"] < 0.02
            ]
            
            return {
                "analyzed_skills": skill_set,
                "average_demand_score": avg_demand_score,
                "average_salary": avg_salary,
                "competition_level": competition_level,
                "skill_details": skill_data,
                "low_demand_skills": low_demand_skills,
                "recommendations": self._generate_competition_recommendations(
                    skill_set, skill_data, competition_level
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing market competition: {e}")
            return {"error": str(e)}
    
    def _generate_competition_recommendations(self, skill_set: List[str], 
                                            skill_data: Dict, competition_level: str) -> List[str]:
        """Generate recommendations based on competition analysis"""
        recommendations = []
        
        if competition_level == "High":
            recommendations.append("Consider specializing in niche areas to reduce competition")
            recommendations.append("Focus on advanced certifications to stand out")
        elif competition_level == "Low":
            recommendations.append("Opportunity to become a market leader in these skills")
            recommendations.append("Consider developing complementary high-demand skills")
        
        # Check for skill gaps
        high_value_skills = [
            skill for skill, data in skill_data.items()
            if data["average_salary"] > 100000
        ]
        
        if high_value_skills:
            recommendations.append(f"Leverage high-value skills: {', '.join(high_value_skills)}")
        
        return recommendations
    
    def get_market_segment_analysis(self, segment: MarketSegment) -> Dict[str, Any]:
        """
        Get analysis for a specific market segment
        
        Args:
            segment: Market segment to analyze
            
        Returns:
            Dictionary with segment analysis
        """
        try:
            if self.market_df.empty:
                return {"error": "No market data available"}
            
            segment_data = self.market_df[self.market_df['market_segment'] == segment.value]
            
            if segment_data.empty:
                return {"error": f"No data for segment '{segment.value}'"}
            
            # Analyze segment
            total_postings = len(segment_data)
            avg_salary = segment_data['avg_salary'].mean()
            
            # Top skills in segment
            skill_counts = segment_data['skill'].value_counts()
            top_skills = skill_counts.head(10).to_dict()
            
            # Experience level distribution
            experience_dist = segment_data['experience_level'].value_counts().to_dict()
            
            # Remote work percentage
            remote_percentage = (segment_data['remote_work'].sum() / total_postings) * 100
            
            return {
                "segment": segment.value,
                "total_postings": total_postings,
                "average_salary": avg_salary,
                "top_skills": top_skills,
                "experience_distribution": experience_dist,
                "remote_work_percentage": remote_percentage,
                "market_share": total_postings / len(self.market_df) * 100
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing market segment: {e}")
            return {"error": str(e)}
    
    def generate_market_report(self, skills: List[str], region: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive market report
        
        Args:
            skills: List of skills to include in report
            region: Optional region filter
            
        Returns:
            Dictionary with comprehensive market report
        """
        try:
            report = {
                "generated_at": datetime.now().isoformat(),
                "report_parameters": {
                    "skills_analyzed": skills,
                    "region_filter": region
                }
            }
            
            # Skill demand analysis
            skill_analyses = {}
            for skill in skills:
                analysis = self.get_skill_demand_analysis(skill)
                if "error" not in analysis:
                    skill_analyses[skill] = analysis
            
            report["skill_demand_analysis"] = skill_analyses
            
            # Salary trend predictions
            salary_predictions = {}
            for skill in skills:
                prediction = self.predict_salary_trends(skill, 6)
                if "error" not in prediction:
                    salary_predictions[skill] = prediction
            
            report["salary_trend_predictions"] = salary_predictions
            
            # Regional insights
            if region:
                regional_insights = self.get_regional_market_insights(region)
                report["regional_insights"] = regional_insights
            else:
                report["regional_insights"] = self.get_regional_market_insights()
            
            # Competition analysis
            competition_analysis = self.analyze_market_competition(skills)
            report["competition_analysis"] = competition_analysis
            
            # Market trends
            trends = {}
            for skill in skills:
                if skill in self.market_trends:
                    trend = self.market_trends[skill]
                    trends[skill] = {
                        "direction": trend.trend_direction.value,
                        "growth_rate": trend.growth_rate,
                        "confidence": trend.prediction_confidence
                    }
            
            report["market_trends"] = trends
            
            # Overall market summary
            report["market_summary"] = {
                "total_postings_analyzed": len(self.market_df),
                "unique_skills": len(self.market_df['skill'].unique()),
                "average_salary_across_market": self.market_df['avg_salary'].mean(),
                "remote_work_percentage": (self.market_df['remote_work'].sum() / len(self.market_df)) * 100
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating market report: {e}")
            return {"error": str(e)}
    
    def visualize_market_trends(self, skills: List[str], save_path: Optional[str] = None):
        """
        Create visualizations for market trends
        
        Args:
            skills: List of skills to visualize
            save_path: Optional path to save visualization
        """
        try:
            if not skills:
                self.logger.warning("No skills provided for visualization")
                return
            
            # Create figure with subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
            
            # 1. Skill demand comparison
            demand_data = []
            for skill in skills:
                analysis = self.get_skill_demand_analysis(skill)
                if "error" not in analysis:
                    demand_data.append({
                        'skill': skill,
                        'demand_score': analysis['demand_score'],
                        'average_salary': analysis['average_salary']
                    })
            
            if demand_data:
                demand_df = pd.DataFrame(demand_data)
                
                # Demand scores
                ax1.bar(demand_df['skill'], demand_df['demand_score'], color='skyblue')
                ax1.set_title('Skill Demand Scores', fontweight='bold')
                ax1.set_ylabel('Demand Score')
                ax1.tick_params(axis='x', rotation=45)
                
                # Average salaries
                ax2.bar(demand_df['skill'], demand_df['average_salary'], color='lightgreen')
                ax2.set_title('Average Salaries by Skill', fontweight='bold')
                ax2.set_ylabel('Salary ($)')
                ax2.tick_params(axis='x', rotation=45)
            
            # 2. Market trends
            trend_data = []
            for skill in skills:
                if skill in self.market_trends:
                    trend = self.market_trends[skill]
                    trend_data.append({
                        'skill': skill,
                        'growth_rate': trend.growth_rate,
                        'salary_trend': trend.salary_trend
                    })
            
            if trend_data:
                trend_df = pd.DataFrame(trend_data)
                
                # Growth rates
                colors = ['green' if x > 0 else 'red' for x in trend_df['growth_rate']]
                ax3.bar(trend_df['skill'], trend_df['growth_rate'], color=colors, alpha=0.7)
                ax3.set_title('Skill Growth Rates', fontweight='bold')
                ax3.set_ylabel('Growth Rate')
                ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                ax3.tick_params(axis='x', rotation=45)
                
                # Salary trends
                colors = ['green' if x > 0 else 'red' for x in trend_df['salary_trend']]
                ax4.bar(trend_df['skill'], trend_df['salary_trend'], color=colors, alpha=0.7)
                ax4.set_title('Salary Trend Rates', fontweight='bold')
                ax4.set_ylabel('Salary Trend Rate')
                ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                ax4.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Market trends visualization saved to {save_path}")
            
            plt.show()
            
        except Exception as e:
            self.logger.error(f"Error visualizing market trends: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Initialize the market analysis system
    analyzer = MarketAnalyzer()
    
    print("=== Job Market Analysis System ===\n")
    
    # 1. Skill demand analysis
    print("1. Skill Demand Analysis:")
    demand_analysis = analyzer.get_skill_demand_analysis()
    if "error" not in demand_analysis:
        print(f"   Total skills analyzed: {demand_analysis['total_skills_analyzed']}")
        print("   Top 5 skills:")
        for skill in demand_analysis['top_skills'][:5]:
            print(f"     - {skill['skill']}: {skill['posting_count']} postings, "
                  f"${skill['average_salary']:,.0f} avg salary")
    print()
    
    # 2. Regional market insights
    print("2. Regional Market Insights:")
    regional_insights = analyzer.get_regional_market_insights()
    if "error" not in regional_insights:
        print(f"   Total regions: {regional_insights['total_regions']}")
        for region in regional_insights['regions'][:3]:
            print(f"     - {region['region']}: {region['total_postings']} postings, "
                  f"${region['average_salary']:,.0f} avg salary")
    print()
    
    # 3. Salary trend predictions
    print("3. Salary Trend Predictions:")
    skills_to_predict = ["Python", "Machine Learning", "SQL"]
    for skill in skills_to_predict:
        prediction = analyzer.predict_salary_trends(skill, 6)
        if "error" not in prediction:
            print(f"   {skill}:")
            print(f"     Current: ${prediction['current_average_salary']:,.0f}")
            print(f"     Predicted (6 months): ${prediction['predicted_salary']:,.0f}")
            print(f"     Growth: {prediction['predicted_growth_rate']:.1%}")
    print()
    
    # 4. Competition analysis
    print("4. Market Competition Analysis:")
    skill_set = ["Python", "Machine Learning", "SQL", "Excel"]
    competition = analyzer.analyze_market_competition(skill_set)
    if "error" not in competition:
        print(f"   Competition Level: {competition['competition_level']}")
        print(f"   Average Demand Score: {competition['average_demand_score']:.3f}")
        print(f"   Average Salary: ${competition['average_salary']:,.0f}")
        print("   Recommendations:")
        for rec in competition['recommendations']:
            print(f"     - {rec}")
    print()
    
    # 5. Market segment analysis
    print("5. Market Segment Analysis:")
    segment_analysis = analyzer.get_market_segment_analysis(MarketSegment.TECHNOLOGY)
    if "error" not in segment_analysis:
        print(f"   Segment: {segment_analysis['segment']}")
        print(f"   Total Postings: {segment_analysis['total_postings']}")
        print(f"   Average Salary: ${segment_analysis['average_salary']:,.0f}")
        print(f"   Remote Work: {segment_analysis['remote_work_percentage']:.1f}%")
    print()
    
    # 6. Generate comprehensive report
    print("6. Generating Comprehensive Market Report...")
    report = analyzer.generate_market_report(["Python", "Machine Learning"], "San Francisco")
    
    if "error" not in report:
        print("   Report generated successfully!")
        print(f"   Skills analyzed: {len(report['skill_demand_analysis'])}")
        print(f"   Total postings: {report['market_summary']['total_postings_analyzed']}")
        print(f"   Market avg salary: ${report['market_summary']['average_salary_across_market']:,.0f}")
    else:
        print(f"   Error: {report['error']}")
    
    print("\n=== Market Analysis Complete ===")
