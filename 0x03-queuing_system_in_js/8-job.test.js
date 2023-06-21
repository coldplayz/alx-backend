import kue from 'kue';
import sinon from 'sinon';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

const testQueue = kue.createQueue();

describe('createPushNotificationsJobs', function () {
  // fixtures
  const testCases = [
    { jobs: [{ one: 1, two: 2 }], type: 'notification', len: 1 },
    { jobs: [{  three: 3, four: 4 }], type: 'notification', len: 1 },
    { jobs: [{ five: 5, six: 6 }, { seven: 7, eigth: 8 }], type: 'notification', len: 2 },
    { jobs: [], type: 'notification', len: 0 },
  ];

  // hooks
  before(function() {
    testQueue.testMode.enter();

    // create spies
    this.clog = sinon.spy(console, 'log');
    this.fn = sinon.spy(createPushNotificationsJobs)
  });

  afterEach(function() {
    testQueue.testMode.clear();

    // restore spies to original state
    sinon.restore();
  });

  after(function() {
    testQueue.testMode.exit()
  });

  // tests
  testCases.forEach(({ jobs, type, len }) => {
    it(`should create different jobs as expected: ${Object.entries(jobs)}`, function () {
      this.fn(jobs, testQueue);

      expect(this.fn.calledWithExactly(jobs, testQueue)).to.be.true;

      if (len === 0) {
        // no job cteated
        expect(testQueue.testMode.jobs.length).to.eq(0);
        return;
      }

      // console.log(this.clog.callCount); // SCAFF
      expect(this.clog.called).to.be.true;
      expect(testQueue.testMode.jobs.length).to.eq(len);
      // expect(this.clog.callCount).to.eq(len);
      if (len >= 2) {
        for (let i = 0; i < len; i++) {
          expect(testQueue.testMode.jobs[i].data).to.deep.equal(jobs[i]);
          expect(testQueue.testMode.jobs[i].type).to.eq(type);
        }
      }
    });
  });

  it('should throw Error on non-array jobs arguments', function () {
    try {
      this.fn('345', testQueue);
    } catch (err) {
      //
    }

    expect(this.fn.threw('Error')).to.be.true;
  });
});
